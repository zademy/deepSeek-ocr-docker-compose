# 📚 DeepSeek OCR - Documentation

Welcome to the complete documentation for DeepSeek OCR!

## 🚀 Quick Navigation

### New to DeepSeek OCR?
👉 **Start here**: [../README.md](../README.md)

### Want to get it running quickly?
👉 **Quick start**: [QUICKSTART.md](QUICKSTART.md) (3 minutes)

### Using Windows?
👉 **Windows guide**: [WINDOWS_SETUP.md](WINDOWS_SETUP.md)

---

## 📖 Documentation Guide

### Getting Started
| Document | Description | Reading Time |
|----------|-------------|--------------|
| [../README.md](../README.md) | 👋 Main project documentation | 5 min |
| [QUICKSTART.md](QUICKSTART.md) | ⚡ Get running in 3 steps | 5 min |
| [WINDOWS_SETUP.md](WINDOWS_SETUP.md) | 🪟 Complete Windows setup guide | 10 min |

### In-Depth Guides
| Document | Description | Reading Time |
|----------|-------------|--------------|
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | 📖 Complete usage manual with examples | 30 min |

---

## 🎯 Documentation by Use Case

### I want to...

#### Use the Web Interface
1. Read [QUICKSTART.md](QUICKSTART.md) to get it running
2. Open http://localhost:3000
3. Check [USAGE_GUIDE.md](USAGE_GUIDE.md) section "Using the Web Interface"

#### Use the API
1. Read [QUICKSTART.md](QUICKSTART.md) to get it running
2. Check [USAGE_GUIDE.md](USAGE_GUIDE.md) section "API Usage"

#### Deploy to Production
1. Read [../SECURITY.md](../SECURITY.md) - Security considerations
2. Read [USAGE_GUIDE.md](USAGE_GUIDE.md) - Production tips

#### Troubleshoot Issues
1. Check [USAGE_GUIDE.md](USAGE_GUIDE.md) - Troubleshooting section
2. If on Windows, check [WINDOWS_SETUP.md](WINDOWS_SETUP.md) - Common Problems

#### Understand the Technology
1. Read [../README.md](../README.md) for overview
2. Review the original repo: https://github.com/deepseek-ai/DeepSeek-OCR

---

## 📚 Documentation Structure

```
docs/
├── README.md              # 👋 This file - documentation index
├── QUICKSTART.md          # ⚡ Quick start guide
├── USAGE_GUIDE.md         # 📖 Complete manual
└── WINDOWS_SETUP.md       # 🪟 Windows setup
```

---

## 🔍 Quick Search

Looking for something specific? Use Ctrl+F (or Cmd+F) in these documents:

- **API examples** → [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Error messages** → [WINDOWS_SETUP.md](WINDOWS_SETUP.md) or [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Performance tips** → [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **OCR modes** → [USAGE_GUIDE.md](USAGE_GUIDE.md)

---

## 🎓 Learning Path

### Beginner Path (Total: ~20 min)
1. [../README.md](../README.md) - 5 min
2. [QUICKSTART.md](QUICKSTART.md) - 5 min
3. Try the web interface - 10 min
4. Read relevant sections of [USAGE_GUIDE.md](USAGE_GUIDE.md) - as needed

### Developer Path (Total: ~45 min)
1. [QUICKSTART.md](QUICKSTART.md) - 5 min
2. [USAGE_GUIDE.md](USAGE_GUIDE.md) - API section - 15 min
3. [../DOCKER_OPTIMIZATION.md](../DOCKER_OPTIMIZATION.md) - 10 min
4. [CONTRIBUTING.md](../CONTRIBUTING.md) - 15 min

### DevOps Path (Total: ~50 min)
1. [QUICKSTART.md](QUICKSTART.md) - 5 min
2. [USAGE_GUIDE.md](USAGE_GUIDE.md) - 20 min
3. [DOCKER_OPTIMIZATION.md](../DOCKER_OPTIMIZATION.md) - 15 min
4. [WINDOWS_SETUP.md](WINDOWS_SETUP.md) - 10 min

---

## 💡 Tips for Reading Documentation

1. **Don't read everything** - Use the table of contents
2. **Start with README.md** - It points you to what you need
3. **Use search** - Ctrl+F is your friend
4. **Follow links** - Documents reference each other
5. **Check examples** - Most guides have practical examples

---

## 🆘 Still Need Help?

1. **Check troubleshooting** sections in:
   - [USAGE_GUIDE.md](USAGE_GUIDE.md#troubleshooting)
   - [WINDOWS_SETUP.md](WINDOWS_SETUP.md#common-problems)

2. **Run the test script**:
   ```bash
   python test_api.py
   ```

3. **Check logs**:
   ```bash
   docker-compose logs -f
   ```

4. **Review the official DeepSeek-OCR repo**:
   - https://github.com/deepseek-ai/DeepSeek-OCR

---

## 📝 Documentation Versions

- **Current Version**: 1.0.0
- **Last Updated**: October 2025
- **Model Version**: DeepSeek-OCR (first release)

---

**Happy reading! 📖**

[← Back to main README](../README.md)

---

## Additional Resources

### GitHub Documentation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute to the project
- [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) - Community guidelines
- [SECURITY.md](../SECURITY.md) - Security policy and reporting
- [LICENSE](../LICENSE) - License information

### API Documentation

When the server is running, interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Need Help?

- Check the [Troubleshooting](../README.md#-troubleshooting) section in the main README
- Open an [issue](../../issues) on GitHub
- Review [existing issues](../../issues?q=is%3Aissue) for similar problems

## Contributing to Documentation

Found a typo or want to improve the docs? Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on submitting improvements.

---

**Note**: All documentation assumes this project is being used for development and testing purposes only.
