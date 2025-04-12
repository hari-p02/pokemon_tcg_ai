# Metals - Heavy Metal Analysis Application

A full-stack application for analyzing heavy metal concentrations in soil and calculating accumulation based on different feedstock applications.

## Project Overview

This application provides tools for:

- Analyzing heavy metal concentrations in soil
- Calculating metal accumulation based on different feedstock types (basalt and peridotite)
- Comparing results against regulatory thresholds
- Visualizing distribution of metal concentrations

## Tech Stack

### Frontend (Client)

- React 19
- TypeScript
- Material-UI (MUI) v7
- Recharts for data visualization
- Vite for build tooling

### Backend (Server)

- FastAPI
- Python 3.x
- Scientific computing libraries:
  - NumPy
  - Pandas
  - SciPy
  - Fitter (for distribution fitting)

## Project Structure

```
.
├── client/                 # Frontend React application
│   ├── src/               # Source code
│   ├── package.json       # Frontend dependencies
│   └── vite.config.ts     # Vite configuration
├── server/                # Backend FastAPI application
│   ├── data/             # Data files
│   ├── heavy_metal_api.py # Main API implementation
│   ├── heavy_metal_tool.py # Core calculation logic
│   └── requirements.txt   # Python dependencies
└── run-dev-tmux.sh       # Development startup script
```

## Client Directory Structure

The client application is organized into several key directories and components:

### Source Directory (`src/`)

```
src/
├── components/           # React components
│   ├── MetalCalculator.tsx       # Main calculator container
│   ├── CalculatorInput.tsx       # Input handling component
│   ├── Charts.tsx               # Data visualization components
│   ├── CustomLegend.tsx         # Custom chart legend
│   ├── CustomParameters.tsx     # Custom calculation parameters form
│   ├── CustomTooltip.tsx       # Custom chart tooltips
│   ├── PresetParameters.tsx    # Preset calculation parameters
│   ├── Regulations.tsx         # Regulatory thresholds display
│   └── ToggleMode.tsx          # Calculator mode toggle
├── services/            # API communication
│   └── metalsService.ts         # Backend API integration
├── assets/             # Static assets
├── App.tsx             # Main application component
└── main.tsx            # Application entry point
```

### Key Components

1. **MetalCalculator (`MetalCalculator.tsx`)**

   - Main container component
   - Manages calculation mode state
   - Coordinates between input and display components

2. **Calculator Components**

   - `CalculatorInput.tsx`: Handles user input validation and submission
   - `CustomParameters.tsx`: Form for detailed custom calculations
   - `PresetParameters.tsx`: Simplified preset calculation options
   - `ToggleMode.tsx`: Switches between preset and custom calculation modes

3. **Visualization Components**
   - `Charts.tsx`: Renders concentration distribution charts
   - `CustomLegend.tsx`: Custom chart legend implementation
   - `CustomTooltip.tsx`: Interactive chart tooltips
   - `Regulations.tsx`: Displays regulatory threshold information

### Services

The `metalsService.ts` provides a comprehensive API client for backend communication:

1. **Data Fetching**

   - `getElements(feedstockType)`: Retrieves available elements for analysis
   - `getThresholds(element)`: Fetches regulatory thresholds

2. **Calculations**

   - `calculateCustomConcentrations(params)`: Performs custom calculations
   - `calculatePresetConcentrations(params)`: Executes preset calculations

3. **Type Definitions**
   - `CustomCalculationParams`: Parameters for custom calculations
   - `PresetCalculationParams`: Parameters for preset calculations
   - `CalculationResult`: Calculation response structure
   - `ThresholdResult`: Regulatory threshold data structure

### Data Flow

1. User input is collected through the calculator components
2. Data is validated and formatted
3. API requests are made through the metals service
4. Results are processed and displayed using the visualization components

## Setup and Installation

### Prerequisites

- Node.js (latest LTS version)
- Python 3.x
- tmux (for development environment)

### Backend Setup

1. Navigate to the server directory:

   ```bash
   cd server
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv  # Try 'python' instead if python3 doesn't work
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the client directory:

   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Development Mode

Use the provided tmux script to start both frontend and backend:

```bash
npm start
```

Or run them separately:

Frontend:

```bash
cd client
npm run dev
```

Backend:

```bash
cd server
python3 run_heavy_metal_api.py
```

## API Endpoints

### GET /elements

- Returns available elements for analysis based on feedstock type
- Query Parameters:
  - feedstock_type: str (basalt or peridotite)

### POST /calculate-preset

- Calculates metal concentrations using preset parameters
- Request Body:
  ```json
  {
    "element": "string",
    "feedstock_type": "string"
  }
  ```

### POST /calculate-custom

- Calculates metal concentrations using custom parameters
- Request Body:
  ```json
  {
    "soil_conc": float,
    "soil_conc_sd": float,
    "soil_d": float,
    "soil_d_err": float,
    "dbd": float,
    "dbd_err": float,
    "feed_conc": float,
    "feed_conc_sd": float,
    "application_rate": float,
    "element": "string",
    "feedstock_type": "string"
  }
  ```

### GET /thresholds

- Returns regulatory thresholds for a specific element
- Query Parameters:
  - element: str

## Core Features

1. **Distribution Analysis**

   - Fits gamma distributions to metal concentration data
   - Calculates probability distributions for soil and feedstock concentrations

2. **Concentration Calculations**

   - Computes feedstock concentration contributions
   - Calculates total element concentrations
   - Handles both preset and custom calculation scenarios

3. **Threshold Comparison**

   - Compares results against regulatory thresholds
   - Categorizes thresholds by extraction method (Total, Aqua Regia, Other)

4. **Visualization**
   - Provides normalized kernel density estimation (KDE) for concentration distributions
   - Supports interactive data visualization
