# Online Library — Frontend

This folder contains the React + TypeScript frontend for the Online Library project. It uses Vite, Tailwind CSS, and React Router for navigation.

---

## Getting Started

**1. Make sure you are in the `frontend` folder:**

```bash
cd frontend
```

**2. Install dependencies:**

```bash
npm install
```

**3. Run the development server:**

```bash
npm run dev
```

Open the browser at the URL displayed (usually `http://localhost:5173`). The app supports hot module reload.

---

## Folder Structure

```
frontend/
├── index.css             # Main Tailwind CSS entry
├── App.tsx               # Root layout (Navbar + Outlet for pages)
├── main.tsx              # Entry point, renders App
├── vite.config.ts        # Vite configuration
├── tsconfig.app.json     # TS config for the app
├── tsconfig.node.json    # TS config for Node environment
├── pages/                # React pages (Catalog, Login, BookDetail, etc.)
├── components/           # Shared components (Navbar, Footer, etc.)
└── assets/               # Static images/icons used in React
```

---

## Commands

| Command | Description |
|---|---|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server with HMR |
| `npm run build` | Build production-ready files |
| `npm run preview` | Preview production build locally |

---

## Styling

Tailwind is configured in `tailwind.config.js` to scan all files in `./index.html` and `./src/**/*.{js,ts,jsx,tsx}`. Custom styles can be added to `index.css` below the Tailwind directives:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom global styles go here */
```

---

## Adding Pages

**1. Create a new file in `pages/` (e.g., `About.tsx`):**

```tsx
import React from "react"

function About() {
  return <div>About Page</div>
}

export default About
```

**2. Add a route in `router.tsx`:**

```ts
{ path: "about", element: <About /> }
```

---

## Notes

- All navigation should use `<Link>` from `react-router-dom` to avoid full page reloads.
- Layout and common elements (like Navbar) should be in `App.tsx` with `<Outlet />`.
- Tailwind utilities should replace most custom CSS — only add custom classes if necessary.