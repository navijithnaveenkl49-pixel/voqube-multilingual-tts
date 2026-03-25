# VoQube - User Interface (UI) Design Guide

This document outlines the design principles, color schemes, typography, and component structure used in the **VoQube** Multilingual Text-to-Speech Generator application.

## 🎨 Design Philosophy
VoQube is designed with a **premium, dark-themed aesthetic** tailored for gamers, streamers, and content creators. The UI focuses on:
- **Glassmorphism & Depth**: Using subtle semi-transparent backgrounds and elevated cards to create a sense of depth against the dark canvas.
- **Vibrant Accents**: High-contrast indigo and purple accents to guide the user's focus to primary actions (e.g., "Generate Voice" button).
- **Responsive Layout**: A fluid layout that adapts seamlessly from mobile devices to large desktop monitors.

## 🖌️ Color Palette
The application utilizes a curated Material UI (MUI) dark theme palette:

| Application Element | Color (Hex / RGB) | Description |
| :--- | :--- | :--- |
| **Primary Accent** | `#6366f1` (Indigo) | Used for primary buttons, active sidebar links, and key highlights. |
| **Secondary Accent**| `#9c27b0` (Purple) | Used for secondary actions and alternative highlights. |
| **Background (Base)** | `#0b0f19` | Deep dark background for the main application canvas. |
| **Surface/Card** | `#111827` | Slightly lighter dark shade for cards, sidebar, and elevated components. |
| **Text (Primary)** | `#ffffff` | Pure white for primary headings and important text. |
| **Text (Secondary)**| `#94a3b8` | Soft slate gray for descriptions, helper text, and inactive icons. |

## 🔤 Typography
- **Primary Font**: Modern sans-serif (system default stack optimized by Material UI - Roboto / Inter).
- **Headings**: Bold (`fontWeight: 600` or `bold`), maximizing readability.
- **Body**: Standard weight for forms, tables, and standard copy.

## 🧩 Core Components

### 1. Navigation (Sidebar - `Layout.jsx`)
- **Width**: `260px` fixed on desktop, hidden in a temporary drawer on mobile.
- **Background**: Solid `#111827`.
- **Active State**: Selected menu items are highlighted with the primary indigo color.
- **User Profile**: A compact card at the bottom displaying the user's avatar, username, and remaining token balance.

### 2. Cards and Containers
- Used extensively in the Dashboard to group logic.
- **Elevation**: Shadow effects (`elevation={2}`) lift the content off the dark background.
- **Border**: Subtle borders or semi-transparent backgrounds (`rgba(255,255,255,0.02)`) create contrast without being solid.

### 3. Audio Player (`Dashboard.jsx`)
- Custom styling applied to the native HTML5 `<audio>` element.
- **CSS Filters**: `filter: 'invert(0.9) hue-rotate(180deg) saturate(2) brightness(1.2)'` applied to invert the default light-themed browser audio player, making it blend perfectly with the dark theme.
- **Container**: Wrapped in a pill-shaped container with an indigo glow effect (`box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3)`).

## 📱 Page Layouts

### Authentication (`Login.jsx`, `Register.jsx`)
- Centered layout using `Container maxWidth="sm"`.
- Clean, focused form inside an elevated card.
- Clear call-to-action text linking between Login and Registration.

### User Dashboard (`Dashboard.jsx`)
- Split-pane layout using MUI's Grid system:
  - **Left Pane (8 columns)**: Text input, Language selection, Voice type dropdown, Auto-translate toggle, and the primary "Generate" button.
  - **Right Pane (4 columns)**: Real-time preview containing the translated text, the stylized audio player, and the "Download" button.

### Admin Panel (`AdminPanel.jsx`)
- **Stat Cards**: Three prominent top cards displaying total users, total generations, and total downloads, using distinct icon colors (Primary, Secondary, Success).
- **Data Table**: A sleek, dark-themed MUI Table displaying registered users, their roles (identified via Chips), token balance, and a quick-edit action button.
- **Modals (Dialog)**: Clean popup modals for modifying user tokens.

## ⚡ Interactive Elements
- **Loading States**: Spinners (`<CircularProgress />`) replace icons inside buttons when processing API requests to provide immediate feedback.
- **Alerts**: Toast-style notifications embedded directly above forms to display API errors.
- **Hover Effects**: Buttons and list items subtly change background colors on mouse hover to indicate interactivity.
