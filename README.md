# 🔑 KeyMate

A **professional, modern Streamlit application** for validating LLM API keys, exploring models, and analyzing model capabilities. Built with advanced UI components that can compete with React.js interfaces.

## 🎯 **Quick Start - Run the Best UI**

### **Single Command to Launch:**
```bash
streamlit run main.py
```

That's it! The application will open in your browser with the most professional and modern UI experience.

---

## ✨ Features

### 🎨 Modern UI Design
- **Professional Interface**: Advanced CSS styling with gradients, animations, and modern design patterns
- **Responsive Layout**: Grid systems and flexbox for optimal viewing on all devices
- **Interactive Components**: Hover effects, transitions, and smooth animations
- **Real-time Notifications**: Toast notifications for user feedback
- **Advanced Filtering**: Search, sort, and filter capabilities for model lists

### 🔑 API Key Validation
- **Multi-Provider Support**: OpenAI, Gemini, Deepseek, Claude, Grok, and Groq
- **Auto-Detection**: Automatically detects provider from API key format
- **Secure Validation**: Keys are never stored or logged
- **Real-time Status**: Live validation with status indicators

### 🤖 Model Management
- **Comprehensive Model Lists**: View all available models for your account
- **Advanced Search**: Search models by name, type, or capabilities
- **Detailed Information**: Rich model details with capabilities and parameters
- **Model Comparison**: Compare different models side-by-side

### 📊 Analytics & Insights
- **Dashboard Metrics**: Real-time statistics and key performance indicators
- **Offline Analysis**: Analyze model IDs without API keys
- **Provider Statistics**: Comprehensive provider information
- **Capability Mapping**: Visual representation of model capabilities

## 🏗️ Clean Project Structure

```
📁 KeyMate/
├── 🚀 main.py                    # Main application entry point
├── 📁 src/                       # Source code
│   ├── 📁 ui/                    # User interface components
│   │   ├── __init__.py
│   │   ├── styling.py           # Modern CSS and styling
│   │   ├── components.py        # Interactive UI components
│   │   └── layout.py            # Layout and navigation
│   ├── 📁 core/                 # Core business logic
│   │   ├── __init__.py
│   │   ├── key_tester.py        # Main API testing logic
│   │   └── 📁 providers/        # Provider-specific testers
│   ├── 📁 config/               # Configuration management
│   │   ├── __init__.py
│   │   ├── app_config.py        # Application settings
│   │   └── demo_config.py       # Demo data and features
│   ├── 📁 utils/                # Utility functions
│   └── 📁 assets/               # Static assets
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                 # This documentation
└── 📄 .gitignore                # Git ignore rules
```

## 🚀 Installation & Setup

### Prerequisites
```bash
python >= 3.8
pip >= 21.0
```

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Launch the application
streamlit run main.py
```

## 🎯 Usage

### 1. API Key Validation
1. Enter your API key in the secure input field
2. Click "Validate" to test the key
3. View provider information and validation status
4. Access your available models

### 2. Model Exploration
1. Browse your available models in the interactive table
2. Use advanced filters to find specific models
3. Select a model to view detailed information
4. Compare models using the comparison tool

### 3. Offline Analysis
1. Enter any model ID for analysis
2. Use quick picks for popular models
3. View parsed model information
4. Analyze provider capabilities

## 🎨 UI Components

### Modern Design Elements
- **Gradient Headers**: Beautiful gradient backgrounds with modern typography
- **Card Containers**: Clean, shadowed containers for content organization
- **Metric Cards**: Professional KPI displays with icons and animations
- **Status Badges**: Color-coded status indicators with gradients
- **Interactive Tables**: Enhanced data tables with search and filtering
- **Provider Badges**: Styled provider indicators with brand colors

### Advanced Features
- **Real-time Notifications**: Toast-style notifications for user feedback
- **Loading States**: Professional loading spinners and progress indicators
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Dark/Light Theme Support**: Automatic theme detection and switching
- **Accessibility**: WCAG compliant design with proper contrast ratios

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set default timeout for API requests
STREAMLIT_SERVER_TIMEOUT=300

# Optional: Configure logging level
STREAMLIT_LOGGER_LEVEL=info

# Optional: Enable demo mode
DEMO_MODE=true
```

### Customization
The UI can be customized by modifying the CSS variables in `src/ui/styling.py`:
- Color schemes and gradients
- Typography and spacing
- Animation durations and effects
- Component styling and layouts

## 📱 Supported Providers

| Provider | Status | Features |
|----------|--------|----------|
| **OpenAI** | ✅ Full Support | API validation, model listing, detailed info |
| **Anthropic Claude** | ✅ Full Support | API validation, model listing, detailed info |
| **Google Gemini** | ✅ Full Support | API validation, model listing, detailed info |
| **Deepseek** | ✅ Full Support | API validation, model listing, detailed info |
| **xAI Grok** | ✅ Full Support | API validation, model listing, detailed info |
| **Groq** | ✅ Full Support | API validation, model listing, detailed info |

## 🛡️ Security

- **No Key Storage**: API keys are never persisted to disk
- **Session State Only**: Keys stored only in Streamlit session state
- **Secure Input**: Password fields for key entry
- **Masked Display**: Keys are masked when displayed
- **No Logging**: No API keys are logged or transmitted

## 🚧 Advanced Features (Coming Soon)

- **Performance Benchmarking**: Compare model performance metrics
- **Cost Analysis**: Estimate API usage costs
- **Usage Analytics**: Track API usage patterns
- **Custom Testing**: Create custom model tests
- **Batch Processing**: Validate multiple keys at once
- **Export Functionality**: Export data in various formats

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for rapid web app development
- Enhanced with [streamlit-extras](https://github.com/arnaudmiribel/streamlit-extras) for additional components
- Designed with modern CSS and responsive principles
- Inspired by professional React.js interfaces

---

## 🎯 **Quick Start Summary**

**To run the application with the best UI experience:**

1. **Clone or download the project**
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Run the app:** `streamlit run main.py`
4. **Enjoy the professional interface!**

The application will automatically:
- ✅ Open in your default browser
- ✅ Provide the most professional UI experience
- ✅ Support all major LLM providers
- ✅ Offer advanced features and analytics

**Made with ❤️ for the AI community**
