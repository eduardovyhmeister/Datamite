# DATAMITE Gradio Chatbot Integration

This document explains how to set up and use the Gradio chatbot that has been integrated into the DATAMITE Django application.

## Overview

The chatbot provides assistance with:
- Data monetization concepts and strategies
- ANP-AHP methodology explanations
- Tool usage guidance
- General support for the DATAMITE platform

## Setup Instructions

### 1. Install Dependencies

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

This will install Gradio along with other required packages.

### 2. Add 'UPLOAD_FOLDER' to .env file
NEW!!
Add a path to a file where to save the vector store. For example to the 'LangGraph_chatbot/data/projects' path

UPLOAD_FOLDER = 'your_file_path'

### 3. Run the Chatbot Server

Start the Gradio chatbot server in a separate terminal:

```bash
python run_chatbot.py
```

Or directly:

```bash
python chatbot_app.py
```

The chatbot will be available at `http://localhost:7860`

### 4. Run the Django Application

In another terminal, start the Django application:

```bash
python manage.py runserver
```

### 5. Access the Chatbot

1. Navigate to the home page of your Django application
2. Click the "Ask our Data Monetization Assistant" button
3. The chatbot will open in a modal window

## Chatbot Features

### Pre-built Responses
The chatbot includes responses for:
- Data monetization questions
- ANP-AHP methodology explanations
- Tool usage guidance
- General help and support

### Example Questions
- "What is data monetization?"
- "How does ANP-AHP work?"
- "How do I use the evaluation tool?"
- "What are the benefits of data monetization?"

## Customization

### Modifying Responses
Edit the `respond()` function in `chatbot_app.py` to customize:
- Response logic
- Keyword matching
- Example questions
- Chatbot appearance

### Styling
The chatbot uses Gradio's Soft theme. You can change this by modifying the `theme` parameter in the `gr.ChatInterface()` call.

### Adding New Features
- Add new response patterns in the `respond()` function
- Include additional examples in the `examples` parameter
- Modify the chatbot title and description

## Deployment Considerations

### Production Deployment
For production deployment:

1. **Separate Servers**: Run the Gradio chatbot on a separate server/port
2. **Domain Configuration**: Update the iframe src in `home.html` to point to your production chatbot URL
3. **Security**: Ensure proper CORS and security headers are configured
4. **Load Balancing**: Consider load balancing for high-traffic scenarios

### Environment Variables
Consider using environment variables for:
- Chatbot server URL
- Port configurations
- API keys (if integrating with external services)

## Troubleshooting

### Common Issues

1. **Chatbot not loading**: Ensure the Gradio server is running and accessible
2. **Modal not opening**: Check browser console for JavaScript errors
3. **Responses not working**: Verify the chatbot server is responding correctly

### Debug Mode
To run the chatbot in debug mode, modify `chatbot_app.py`:

```python
demo.launch(server_name="0.0.0.0", server_port=7860, share=True, debug=True)
```

## Integration with Django

The chatbot is integrated into the Django application through:
- A button in the home page template (`ANPAHP/templates/home.html`)
- JavaScript modal functionality
- Iframe embedding of the Gradio widget

The integration is designed to be non-intrusive and can be easily disabled by commenting out the chatbot button section in the template.

## Future Enhancements

Potential improvements:
- User authentication integration
- Conversation history storage
- Advanced NLP capabilities
- Multi-language support
- Integration with external AI services 