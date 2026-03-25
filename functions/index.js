const functions = require("firebase-functions");
const admin = require("firebase-admin");
const { MsEdgeTTS } = require("msedge-tts");
const translate = require("@vitalets/google-translate-api");
const { v4: uuidv4 } = require("uuid");
const os = require("os");
const path = require("path");
const fs = require("fs");

admin.initializeApp();

const db = admin.firestore();
const storage = admin.storage().bucket();

// Voice mapping similar to the Python backend
const LANGUAGE_VOICES = {
  "English": { "Female": "en-US-AriaNeural", "Male": "en-US-GuyNeural" },
  "Hindi": { "Female": "hi-IN-SwaraNeural", "Male": "hi-IN-MadhurNeural" },
  "Tamil": { "Female": "ta-IN-PallaviNeural", "Male": "ta-IN-ValluvarNeural" },
  "Malayalam": { "Female": "ml-IN-SobhanaNeural", "Male": "ml-IN-MidhunNeural" },
  "Telugu": { "Female": "te-IN-ShrutiNeural", "Male": "te-IN-MohanNeural" },
  "Kannada": { "Female": "kn-IN-SapnaNeural", "Male": "kn-IN-GaganNeural" },
  "Bengali": { "Female": "bn-IN-TanishaaNeural", "Male": "bn-IN-BashkarNeural" },
  "Marathi": { "Female": "mr-IN-AarohiNeural", "Male": "mr-IN-ManoharNeural" },
  "Gujarati": { "Female": "gu-IN-DhwaniNeural", "Male": "gu-IN-NiranjanNeural" },
  "Punjabi": { "Female": "pa-IN-OjasNeural", "Male": "pa-IN-AmanNeural" },
  "Spanish": { "Female": "es-ES-ElviraNeural", "Male": "es-ES-AlvaroNeural" },
  "French": { "Female": "fr-FR-DeniseNeural", "Male": "fr-FR-HenriNeural" },
  "German": { "Female": "de-DE-KatjaNeural", "Male": "de-DE-ConradNeural" },
  "Urdu": { "Female": "ur-PK-UzmaNeural", "Male": "ur-PK-AsadNeural" },
  "Japanese": { "Female": "ja-JP-NanamiNeural", "Male": "ja-JP-KeitaNeural" },
  "Korean": { "Female": "ko-KR-SunHiNeural", "Male": "ko-KR-InJoonNeural" },
  "Chinese": { "Female": "zh-CN-XiaoxiaoNeural", "Male": "zh-CN-YunxiNeural" },
};

const LANG_MAP = {
  "English": "en", "Hindi": "hi", "Tamil": "ta", "Malayalam": "ml", "Telugu": "te",
  "Kannada": "kn", "Bengali": "bn", "Marathi": "mr", "Gujarati": "gu", "Punjabi": "pa",
  "Spanish": "es", "French": "fr", "German": "de", "Urdu": "ur", "Japanese": "ja",
  "Korean": "ko", "Chinese": "zh-CN",
};

/**
 * Handle user creation and initialize profile in Firestore
 */
exports.onUserCreate = functions.auth.user().onCreate(async (user) => {
  const userProfile = {
    uid: user.uid,
    username: user.displayName || user.email.split("@")[0],
    email: user.email,
    role: "user", // default role
    free_generations_left: 10,
    created_at: admin.firestore.FieldValue.serverTimestamp(),
  };

  // If this email is a known admin, set role (optional)
  // if (user.email === "admin@voqube.app") userProfile.role = "admin";

  return db.collection("users").doc(user.uid).set(userProfile);
});

/**
 * Main TTS Generation Callable Function
 */
exports.generateVoice = functions.https.onCall(async (data, context) => {
  // Check auth
  if (!context.auth) {
    throw new functions.https.HttpsError("unauthenticated", "User must be logged in.");
  }

  const { text, language, voice_type, auto_translate } = data;
  const uid = context.auth.uid;

  // 1. Check user tokens
  const userDoc = await db.collection("users").doc(uid).get();
  const userData = userDoc.data();

  if (userData.free_generations_left <= 0 && userData.role !== "admin") {
    throw new functions.https.HttpsError("resource-exhausted", "No free generations left.");
  }

  try {
    // 2. Translation
    let translatedText = text;
    if (auto_translate && language !== "English") {
      const targetCode = LANG_MAP[language] || "en";
      const result = await translate(text, { to: targetCode });
      translatedText = result.text;
    }

    // 3. TTS Generation
    const voiceName = LANGUAGE_VOICES[language]?.[voice_type] || "en-US-AriaNeural";
    const tts = new MsEdgeTTS();
    await tts.setMetadata(voiceName, "audio-24khz-48kbitrate-mono-mp3");

    const tempFilePath = path.join(os.tmpdir(), `${uuidv4()}.mp3`);
    await tts.toFile(tempFilePath, translatedText);

    // 4. Upload to Firebase Storage
    const storagePath = `audio/${uid}/${path.basename(tempFilePath)}`;
    const [file] = await storage.upload(tempFilePath, {
      destination: storagePath,
      metadata: { contentType: "audio/mpeg" },
    });

    // Make file public or get a signed URL (simpler for this demo)
    await file.makePublic();
    const publicUrl = `https://storage.googleapis.com/${storage.name}/${storagePath}`;

    // 5. Update DB
    const generation = {
      user_id: uid,
      text,
      translated_text: translatedText !== text ? translatedText : null,
      language,
      voice_type,
      file_path: publicUrl,
      is_deleted: false,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
    };

    const genRef = await db.collection("generations").add(generation);

    if (userData.role !== "admin") {
      await db.collection("users").doc(uid).update({
        free_generations_left: admin.firestore.FieldValue.increment(-1),
      });
    }

    // 6. Cleanup temp file
    fs.unlinkSync(tempFilePath);

    return { id: genRef.id, ...generation };

  } catch (error) {
    console.error("TTS Generation Error:", error);
    throw new functions.https.HttpsError("internal", error.message);
  }
});

/**
 * Tracking Downloads
 */
exports.trackDownload = functions.https.onCall(async (data, context) => {
  if (!context.auth) throw new functions.https.HttpsError("unauthenticated", "Must be logged in.");
  
  const { generation_id } = data;
  const uid = context.auth.uid;

  await db.collection("downloads").add({
    user_id: uid,
    generation_id,
    created_at: admin.firestore.FieldValue.serverTimestamp(),
  });

  return { status: "success" };
});
