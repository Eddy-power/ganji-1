# Korean Lunar Calendar Converter

## Overview

This is a Flask-based web application that converts dates between the Korean solar (양력) and lunar (음력) calendar systems. The application provides a simple web interface for users to input dates in either calendar system and receive the corresponding date in the other system, along with traditional Korean and Chinese GapJa (sexagenary cycle) information. It supports intercalation (윤달/leap months) in lunar calendar calculations.

## Recent Changes (2025-11-30)
- Created Flask web application with beautiful responsive UI
- Added date input form with year/month/day fields
- Added 양력(solar)/음력(lunar) selection buttons
- Added 윤달(intercalation) checkbox option for lunar dates
- Displays both solar and lunar dates with Korean and Chinese GapJa (간지)

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Single-Page Application Pattern**
- Uses vanilla JavaScript with a template-based approach
- Server-side rendering via Flask's Jinja2 templating engine
- No JavaScript framework dependencies (React, Vue, etc.)
- Responsive CSS with gradient design aesthetic

**Rationale**: Keeps the application lightweight and simple for a single-purpose conversion tool. The lack of complex state management requirements makes a framework unnecessary.

### Backend Architecture

**Flask Microframework Pattern**
- Minimal Flask application with REST API endpoint
- Stateless request handling
- JSON-based API communication

**API Structure**:
- `GET /` - Serves the main HTML interface
- `POST /convert` - Accepts date conversion requests and returns results

**Caching Strategy**:
- Aggressive cache prevention via HTTP headers
- `Cache-Control`, `Pragma`, and `Expires` headers all configured to prevent caching
- Applied globally via `@app.after_request` decorator

**Rationale**: The cache-busting approach ensures users always see fresh data, which is critical for a date conversion tool where accuracy is paramount. The stateless design allows for easy horizontal scaling if needed.

### Data Processing

**Korean Lunar Calendar Library Integration**
- Core conversion logic delegated to `korean-lunar-calendar` Python package
- Supports bidirectional conversion (solar ↔ lunar)
- Handles intercalation months (leap months in lunar calendar)

**Date Input Processing**:
- Year, month, day components parsed as integers
- Calendar type selection (solar/lunar)
- Optional intercalation flag for lunar dates

**Date Output Format**:
- ISO format dates for both solar and lunar calendars
- Korean GapJa strings (traditional Korean sexagenary cycle)
- Chinese GapJa strings (traditional Chinese sexagenary cycle)
- Intercalation status indicator

**Rationale**: Leveraging an established library for complex lunar calendar calculations avoids reimplementing intricate astronomical algorithms and ensures accuracy across edge cases.

### Error Handling

**Current Implementation**:
- Try-catch block wraps conversion logic
- Success flag returned in JSON responses

**Known Limitation**: The app.py file appears truncated and incomplete error handling logic is visible. Full implementation would include proper exception handling and user-friendly error messages.

## External Dependencies

### Python Packages

**Flask** - Web framework
- Provides routing, templating, and request handling
- Lightweight and suitable for small applications

**korean-lunar-calendar** - Core conversion library
- Handles all calendar conversion algorithms
- Provides GapJa (sexagenary cycle) calculations
- Supports intercalation month detection
- Source: https://pypi.org/project/korean-lunar-calendar/

### Frontend Dependencies

**Noto Sans KR Font** (implied by CSS)
- Korean language font support
- Likely loaded via Google Fonts CDN

### No Database

This application does not use persistent data storage. All conversions are performed on-demand using algorithmic calculations from the korean-lunar-calendar library.