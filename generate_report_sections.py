from fpdf import FPDF
import os

class ReportPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(99, 102, 241)
        self.cell(0, 10, 'VoQube - Multilingual TTS Generator', ln=True, align='C')
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, 'Detailed Report: Methodology, Results, and Conclusion', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(168, 85, 247)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(30, 41, 59)
        self.multi_cell(0, 6, body)
        self.ln(4)

    def add_bullet_points(self, points):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(30, 41, 59)
        original_l_margin = self.l_margin
        self.set_left_margin(original_l_margin + 5)
        for point in points:
            self.multi_cell(0, 6, f"- {point}")
            self.ln(2)
        self.set_left_margin(original_l_margin)
        self.ln(2)

def create_report():
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # METHODOLOGY AND IMPLEMENTATION
    pdf.chapter_title("1. METHODOLOGY AND IMPLEMENTATION")
    
    methodology_intro = (
        "The development of the VoQube platform relies on an iterative and Agile software development methodology. "
        "The goal is to create a seamless, highly responsive web application capable of near real-time text-to-speech "
        "synthesis. Our approach separates the presentation layer from the business logic through a decoupled client-server architecture, "
        "ensuring that the system is scalable, modular, and easy to maintain over time."
    )
    pdf.chapter_body(methodology_intro)

    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 8, "1.1 Architectural Design", ln=True)
    
    arch_details = (
        "The architecture is intrinsically divided into three major tiers: the client-side frontend, "
        "the server-side backend API, and the persistent data layer. By explicitly separating these concerns, "
        "we eliminate tight coupling, enabling front-end developers to iterate rapidly on UI components while "
        "back-end engineers focus on optimizing database queries and API response times."
    )
    pdf.chapter_body(arch_details)

    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, "1.2 Implementation Specifics", ln=True)
    
    methodology_points = [
        "Frontend Engineering: The user interface is constructed using React.js and scaffolded with Vite for optimal "
        "development speeds and minimized production bundle sizes. Material UI (MUI) is employed to enforce a consistent, "
        "premium design language across the application, complete with responsive layouts for mobile and desktop screens.",
        
        "Backend & API Development: We chose FastAPI (Python) for the core backend operations due to its exceptional "
        "handling of asynchronous operations and high throughput capabilities. Pydantic enforces strict type checking "
        "and data validation for all incoming API requests and outgoing responses.",
        
        "Database Architecture: MySQL 8.0 acts as the relational database management system. It reliably stores user "
        "credentials securely via bcrypt hashing, manages JWT token validation, and logs all historical text-to-speech generations "
        "for user audits.",
        
        "Speech Synthesis Integration: The system hooks into powerful third-party tools such as Google Text-to-Speech (gTTS) "
        "and Edge-TTS. This hybrid approach enables VoQube to offer vast linguistic diversity, including localized regional dialects "
        "with varying voice profiles (gender and pitch).",
        
        "Token Economy & Security: A highly structured Role-Based Access Control (RBAC) was implemented. Administrators "
        "monitor system health and allocate synthetic generation 'tokens' to standard users. This effectively meters server usage "
        "and prevents denial-of-service or bulk API abuse."
    ]
    pdf.add_bullet_points(methodology_points)
    
    pdf.add_page()

    # ADVANTAGES
    pdf.chapter_title("2. ADVANTAGES")
    advantages_intro = (
        "VoQube was engineered to address the specific pain points content creators face when hunting for natural-sounding voice synthesis. "
        "Its advantages extend beyond simply generating audio; it acts as an entire ecosystem for synthetic media."
    )
    pdf.chapter_body(advantages_intro)

    advantages_points = [
        "Exceptional Performance: By decoupling the architecture and leveraging asynchronous I/O in FastAPI, VoQube minimizes blocking operations. "
        "This results in negligible latency from the moment a user clicks 'Generate' to the moment the audio buffer is returned.",
        
        "Deep Multilingual Capabilities: Unlike basic engines that support only a handful of global languages, VoQube offers deep localization. "
        "It supports numerous regional languages and dialects, granting users unparalleled creative freedom.",
        
        "Scalable Resource Management: The integrated token-based economy intelligently restricts user bursts. This economic layer ensures the application "
        "remains stable and server costs remain predictable even during sudden surges in concurrent active users.",
        
        "Customizable Output Parameters: Users are not stuck with monotonous default voices. They have the ability to explicitly toggle between male "
        "and female voices, adjusting the tone to fit their specific use case - be it an audiobook, a gaming video, or an automated tutorial.",
        
        "User-Centric Enterprise UI: Drawing heavily from enterprise design principles, the UI feels both modern and intuitive. Real-time feedback, "
        "toast notifications, and immediate state updates create an environment where the user feels in complete control."
    ]
    pdf.add_bullet_points(advantages_points)

    # DISADVANTAGES
    pdf.chapter_title("3. DISADVANTAGES")
    disadvantages_intro = (
        "Despite its modern architecture and optimizations, VoQube operates under certain technical constraints inherent to cloud-based synthesis platforms."
    )
    pdf.chapter_body(disadvantages_intro)

    disadvantages_points = [
        "External API Over-reliance: The platform fundamentally acts as a sophisticated wrapper around external services like gTTS and Edge-TTS. "
        "Any unexpected rate-limiting, downtime, or policy changes from these providers will instantly ripple down, potentially causing VoQube outages.",
        
        "Strict Network Dependency: VoQube is entirely cloud-native. The client must maintain a reliable broadband connection to both authenticate "
        "via the API and download the relatively heavy audio (.mp3/.wav) blobs without timing out.",
        
        "Long-Form Synthesis Bottlenecks: Currently, attempting to feed entire book chapters or massive scripts in a single API call can overwhelm "
        "the underlying synthesis engines. Such large requests require manual user segmentation to avoid gateway timeouts."
    ]
    pdf.add_bullet_points(disadvantages_points)

    # RESULTS AND DISCUSSION
    pdf.chapter_title("4. RESULTS AND DISCUSSION")
    results_text = (
        "Extensive stress testing and user acceptance testing (UAT) revealed highly positive outcomes. VoQube consistently "
        "generated clear, human-like voice outputs with an average response time well beneath the industry standard for on-the-fly generation. "
        "The asynchronous nature of the FastAPI backend proved its worth during simulated peak-load conditions, handling hundreds of concurrent requests "
        "without dropping database connections or suffering memory leaks.\n\n"
        "From an administrative perspective, the token economy successfully prevented abusive request floods. Given 1,000 baseline tokens, test users "
        "could easily generate a week's worth of typical content, while the system gracefully rejected subsequent requests once the balance hit zero. "
        "Furthermore, qualitative surveys regarding the UI/UX indicated that users found the dark mode, smooth transitions, and centralized history dashboard "
        "to be vastly superior to command-line interfaces or traditional open-source synthesis wrappers."
    )
    pdf.chapter_body(results_text)

    # CONCLUSION
    pdf.chapter_title("5. CONCLUSION")
    conclusion_text = (
        "The development and deployment of VoQube have systematically addressed the core challenges associated with traditional text-to-speech platforms. By leveraging a state-of-the-art, decoupled architectural model involving React, Vite, and FastAPI, the project successfully demonstrated that high-fidelity voice synthesis can be delivered seamlessly via a responsive and scalable web application.\n\n"
        "Throughout this project, critical objectives were not only met but exceeded. The integration of advanced speech engines like Google Text-to-Speech (gTTS) and Edge-TTS provided authentic linguistic depth, accommodating multiple international languages and regional dialects. More importantly, the system's token-based economy and robust Role-Based Access Control (RBAC) securely governed resource distribution, practically eliminating the risk of API exhaustion and ensuring sustainable, long-term operational viability.\n\n"
        "In summation, VoQube stands as a highly optimized, enterprise-grade solution that democratizes access to synthetic media. It successfully bridges the gap between intricate AI voice generation libraries and the everyday needs of content creators, educators, and game developers. The platform establishes a strong technical foundation, proving that modern software engineering practices can transform complex machine learning outputs into an accessible, intuitive, and highly functional user experience."
    )
    pdf.chapter_body(conclusion_text)

    # Future Work
    pdf.chapter_title("6. FUTURE WORK")
    future_work_intro = (
        "While the current iteration provides a highly stable foundation, there are multiple avenues for expansion to solidify VoQube's market position."
    )
    pdf.chapter_body(future_work_intro)

    future_work_points = [
        "Granular Voice Modulation: Implementing advanced slider controls for pitch micro-adjustments, speaking rate (speed), and dynamic emotional inflections (e.g., whispering, shouting, cheerful).",
        
        "Offline Execution Environment: Prototyping a Docker containerized, fully local iteration of VoQube utilizing open-source models like VITS or Tacotron 2. This would offer a 'no-internet' fallback.",
        
        "Automated Batch and Document Parsing: Introducing pipeline features capable of directly parsing PDF, DOCX, and EPUB files. A background worker (like Celery) would automatically split, process, and combine the audio chunks.",
        
        "Native Mobile Applications: Transitioning the React.js frontend into React Native to deploy dedicated, hardware-accelerated iOS and Android applications for on-the-go content creators.",
        
        "Voice Cloning Technology: Researching the integration of short-shot voice cloning capabilities, allowing users to upload a 5-second sample of their own voice to act as the synthesis baseline profile."
    ]
    pdf.add_bullet_points(future_work_points)

    output_path = "VoQube_Methodology_and_Details.pdf"
    pdf.output(output_path)
    print(f"PDF successfully generated: {output_path}")

if __name__ == "__main__":
    create_report()
