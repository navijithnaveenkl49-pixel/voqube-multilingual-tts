import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";
import { getFunctions } from "firebase/functions";

// Your real Firebase project config
const firebaseConfig = {
  apiKey: "AIzaSyBjKcVv8XLBmOyXPmPZ9thlS3aWJw4tdDw",
  authDomain: "voqube-f1a50.firebaseapp.com",
  projectId: "voqube-f1a50",
  storageBucket: "voqube-f1a50.firebasestorage.app",
  messagingSenderId: "1044095077896",
  appId: "1:1044095077896:web:8ab95607f95f1551678bbd",
  measurementId: "G-QQN06S150E"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);
export const functions = getFunctions(app);

export default app;
