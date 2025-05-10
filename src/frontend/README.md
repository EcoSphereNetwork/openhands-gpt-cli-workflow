# OpenHands GPT-CLI Workflow Frontend

This is the frontend for the OpenHands GPT-CLI Workflow integration. It provides a user interface for managing the workflow between OpenHands, GPT-CLI, and Dev-Server-Workflow.

## Features

- Dashboard with system overview
- Repository management
- Issue tracking and management
- Dev-Server control panel
- Workflow monitoring
- Settings configuration

## Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

The application will be available at http://localhost:54139.

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
src/
├── assets/           # Static assets
├── components/       # Reusable UI components
├── contexts/         # React contexts
├── hooks/            # Custom React hooks
├── pages/            # Page components
├── services/         # API services
├── utils/            # Utility functions
├── App.tsx           # Main application component
├── main.tsx          # Application entry point
└── theme.ts          # Material UI theme configuration
```

## Integration with Backend

The frontend communicates with the OpenHands API and the Dev-Server-Workflow API through the services defined in `src/services/api.ts`. The API endpoints are proxied through Vite's development server to avoid CORS issues.

## Technologies Used

- React
- TypeScript
- Material UI
- React Router
- Axios
- Vite

## License

MIT