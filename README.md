# Financial Analyses Website

## Overview

This is a comprehensive financial analysis platform built with Streamlit that provides portfolio management, technical analysis, and dividend tracking capabilities for Turkish and international markets. The application focuses on stock and ETF analysis with Turkish language support and localization.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **Multi-page Structure**: Uses Streamlit's pages feature with dedicated modules for:
  - Portfolio Management (📊_Portfolio.py)
  - Technical Analysis (📈_Analiz.py) 
  - Dividend Tracking (💰_Temettü.py)
- **Theme Support**: Light/dark theme toggle with persistent state
- **Responsive Layout**: Wide layout with sidebar navigation and column-based responsive design

### Backend Architecture
- **Modular Design**: Utility classes organized in `/utils` directory
- **Data Layer**: Yahoo Finance API integration via yfinance library
- **Business Logic**: Separated into specialized managers:
  - DataFetcher: Market data retrieval and caching
  - PortfolioManager: Portfolio operations and state management
  - TechnicalAnalysis: Technical indicators and calculations
  - TurkishLocale: Localization and translation services

### Key Components

#### Data Management
- **DataFetcher Class**: Handles all external API calls to Yahoo Finance
- **Caching Strategy**: 5-minute TTL caching using Streamlit's cache_data decorator
- **Error Handling**: Graceful degradation with user-friendly error messages
- **Session State**: Portfolio data persistence across page navigation

#### Portfolio Management
- **Position Tracking**: Add, update, and remove portfolio positions
- **Performance Metrics**: Real-time portfolio valuation and P&L calculations
- **Target Management**: Set and track target quantities for positions

#### Technical Analysis
- **Indicators**: EMA, SMA, RSI calculations
- **Chart Visualization**: Interactive Plotly charts with technical overlays
- **Multi-timeframe Analysis**: Support for various periods and intervals

#### Localization
- **Turkish Language Support**: Complete Turkish translation for financial terms
- **Date Formatting**: Turkish month and day name translations
- **Market Terms**: Comprehensive financial terminology mapping

## Data Flow

1. **User Input**: Symbol entry and parameter selection via Streamlit interface
2. **Data Retrieval**: DataFetcher queries Yahoo Finance API with caching
3. **Processing**: Technical indicators calculated and portfolio metrics computed
4. **Visualization**: Plotly charts render processed data
5. **State Management**: Portfolio changes persisted in Streamlit session state

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **yfinance**: Yahoo Finance API client for market data
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive charting and visualization
- **numpy**: Numerical computations

### Data Sources
- **Yahoo Finance**: Primary market data source for stocks, ETFs, and market indices
- **No Database**: Application uses session state for data persistence (stateless design)

## Deployment Strategy

### Replit Configuration
- **Runtime**: Python 3.11 with Nix package management
- **Port Configuration**: Application runs on port 5000
- **Auto-scaling**: Configured for autoscale deployment target
- **Process Management**: UV package manager for dependency resolution

### Development Workflow
- **Hot Reload**: Streamlit's built-in hot reload for development
- **Package Management**: UV lock file for reproducible builds
- **Modular Structure**: Easy to extend with new analysis features

### Architectural Decisions

#### Choice of Streamlit over Traditional Web Frameworks
- **Problem**: Need for rapid development of data visualization application
- **Solution**: Streamlit for Python-native web development
- **Rationale**: Reduces complexity, excellent for data apps, built-in state management
- **Trade-offs**: Less customization flexibility but much faster development

#### Yahoo Finance API Integration
- **Problem**: Need reliable, free market data source
- **Solution**: yfinance library for Yahoo Finance access
- **Rationale**: Comprehensive data coverage, no API key required, good Turkish market support
- **Trade-offs**: Rate limiting concerns, data quality dependent on Yahoo

#### Session State for Portfolio Management
- **Problem**: Need persistent portfolio data without database complexity
- **Solution**: Streamlit session state for in-memory persistence
- **Rationale**: Simplifies deployment, reduces infrastructure requirements
- **Trade-offs**: Data lost on session end, not suitable for production user management

#### Modular Utility Structure
- **Problem**: Code organization and reusability across pages
- **Solution**: Separated utility classes in `/utils` directory
- **Rationale**: Promotes code reuse, easier testing, clear separation of concerns
- **Benefits**: Maintainable codebase, extensible architecture
