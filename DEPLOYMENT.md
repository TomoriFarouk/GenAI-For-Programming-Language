# 🚀 Deployment Guide: Hugging Face Spaces

## Quick Start (5 minutes)

### Step 1: Prepare Your Repository
1. **Create a GitHub repository** with your project files
2. **Upload all files** from this directory to your GitHub repo
3. **Make sure you have**:
   - `app.py` (main Streamlit app)
   - `fine.py` (AI tutor implementation)
   - `requirements.txt` (dependencies)
   - `README.md` (documentation)

### Step 2: Create Hugging Face Space
1. **Go to** [huggingface.co/spaces](https://huggingface.co/spaces)
2. **Click** "Create new Space"
3. **Fill in the details**:
   - **Owner**: Your HF username
   - **Space name**: `ai-programming-tutor`
   - **License**: Choose appropriate license
   - **SDK**: Select **Streamlit**
   - **Python version**: 3.10
4. **Click** "Create Space"

### Step 3: Connect Your Repository
1. **In your Space settings**, go to "Repository" tab
2. **Select** "GitHub repository"
3. **Choose** your GitHub repository
4. **Set the main file** to `app.py`
5. **Click** "Save"

### Step 4: Upload Your Fine-tuned Model
1. **In your Space**, go to "Files" tab
2. **Create a folder** called `model`
3. **Upload your fine-tuned model files**:
   - `model-00001-of-00006.safetensors`
   - `model-00002-of-00006.safetensors`
   - `model-00003-of-00006.safetensors`
   - `model-00004-of-00006.safetensors`
   - `model-00005-of-00006.safetensors`
   - `model-00006-of-00006.safetensors`
   - `config.json`
   - `tokenizer.json`
   - `tokenizer.model`
   - `tokenizer_config.json`
   - `special_tokens_map.json`
   - `generation_config.json`

### Step 5: Update Model Path
1. **Edit** `app.py` in your Space
2. **Change the model path** to:
   ```python
   model_path = "./model"  # Path to uploaded model
   ```
3. **Save** the changes

### Step 6: Deploy
1. **Your Space will automatically build** and deploy
2. **Wait for the build to complete** (5-10 minutes)
3. **Your app will be live** at: `https://huggingface.co/spaces/YOUR_USERNAME/ai-programming-tutor`

## 🎯 Advanced Configuration

### Hardware Settings
- **CPU**: Default (sufficient for inference)
- **GPU**: T4 (recommended for faster inference)
- **Memory**: 16GB+ (required for 7B model)

### Environment Variables
Add these in your Space settings:
```
TOKENIZERS_PARALLELISM=false
DATASETS_DISABLE_MULTIPROCESSING=1
```

### Custom Domain (Optional)
1. **In Space settings**, go to "Settings" tab
2. **Enable** "Custom domain"
3. **Add your domain** (e.g., `tutor.yourdomain.com`)

## 🔧 Troubleshooting

### Common Issues

**Issue**: Model not loading
- **Solution**: Check model path and file structure
- **Debug**: Look at Space logs in "Settings" → "Logs"

**Issue**: Out of memory
- **Solution**: Upgrade to GPU hardware
- **Alternative**: Use demo mode

**Issue**: Build fails
- **Solution**: Check `requirements.txt` for missing dependencies
- **Debug**: Review build logs

### Performance Optimization

1. **Enable GPU** in Space settings
2. **Use model quantization** for faster inference
3. **Implement caching** for repeated requests
4. **Add rate limiting** to prevent abuse

## 📊 Monitoring

### Usage Analytics
- **View usage** in Space settings
- **Monitor performance** with built-in metrics
- **Track user engagement** through logs

### Cost Management
- **Free tier**: 16 hours/month GPU time
- **Pro tier**: $9/month for unlimited GPU
- **Enterprise**: Custom pricing

## 🌐 Sharing Your App

### Public Access
1. **Set Space to public** in settings
2. **Share the URL** with users
3. **Add to HF Spaces showcase**

### Embedding
```html
<iframe
  src="https://huggingface.co/spaces/YOUR_USERNAME/ai-programming-tutor"
  width="100%"
  height="800px"
  frameborder="0"
></iframe>
```

## 🔒 Security Considerations

1. **Input validation** for code submissions
2. **Rate limiting** to prevent abuse
3. **Content filtering** for inappropriate code
4. **User authentication** (optional)

## 📈 Scaling

### For High Traffic
1. **Upgrade to Pro tier** for unlimited GPU
2. **Implement caching** with Redis
3. **Use load balancing** for multiple instances
4. **Monitor performance** and optimize

### For Production Use
1. **Add user authentication**
2. **Implement logging** and analytics
3. **Set up monitoring** and alerts
4. **Create backup** and recovery procedures

## 🎉 Success!

Your AI Programming Tutor is now live and accessible to students worldwide! 

**Next steps**:
1. **Test thoroughly** with different code examples
2. **Gather user feedback** and iterate
3. **Share with your target audience**
4. **Monitor usage** and improve based on data

## 📞 Support

- **Hugging Face Docs**: [docs.huggingface.co](https://docs.huggingface.co)
- **Spaces Documentation**: [huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
- **Community Forum**: [discuss.huggingface.co](https://discuss.huggingface.co) 