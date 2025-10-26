# Security Policy

## ⚠️ Development and Testing Only

**IMPORTANT:** This software is intended for **development and testing purposes ONLY**. It is NOT designed for production use and should NOT be deployed in production environments without significant additional security hardening.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Known Security Considerations

### For Development/Testing Environments

This project has the following security characteristics suitable for development only:

1. **No Authentication** - API endpoints are open without authentication
2. **No Rate Limiting** - No protection against abuse
3. **File Upload** - Basic validation only, not hardened for production
4. **CORS** - Configured to allow all origins
5. **Error Messages** - May expose system information

### If Adapting for Production

**DO NOT use this software in production without implementing:**

- ✅ Authentication and authorization (OAuth2, JWT, API keys)
- ✅ Rate limiting and DDoS protection
- ✅ Input validation and sanitization
- ✅ Secure file upload handling
- ✅ HTTPS/TLS encryption
- ✅ Security headers (CSP, HSTS, X-Frame-Options, etc.)
- ✅ Logging and monitoring
- ✅ Data encryption at rest and in transit
- ✅ Regular security audits
- ✅ Dependency vulnerability scanning

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email the details to: [Create an issue with `security` label]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- Initial response: Within 48 hours
- Status update: Within 7 days
- Fix timeline: Depends on severity and complexity

## Security Best Practices for Users

### Development Environment

- Run containers with minimal privileges
- Use Docker security features (AppArmor, seccomp)
- Keep Docker and dependencies updated
- Don't expose ports publicly
- Use firewall rules to restrict access

### Data Handling

- Don't process sensitive or personal data
- Clear uploaded files regularly
- Don't store production data in dev environment
- Be aware of data privacy regulations (GDPR, CCPA)

### Network Security

- Run on isolated networks (localhost or private networks only)
- Don't expose to the internet
- Use VPN for remote access
- Monitor network traffic

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY SECURITY GUARANTEES. Users assume all risks associated with security vulnerabilities. The maintainers are not responsible for any security breaches, data loss, or damages resulting from use of this software.

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

Last updated: October 2025
