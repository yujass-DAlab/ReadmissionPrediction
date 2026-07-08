# Security Policy

## Supported Versions

Currently, only the latest version of this project is actively supported with security updates.

| Version | Supported |
| :--- | :--- |
| 1.0.0 (Latest) | ✅ |
| Older versions | ❌ |

---

## Reporting a Vulnerability

I take the security of this project seriously, especially given its healthcare context. If you discover a security vulnerability, please **do not** open a public GitHub issue.

Instead, please send an email to: **[yujass73@gmai.com]** with the subject line: `[Security] Readmission Predictor`.

I will respond to your report within **48 hours** and work with you to understand and resolve the issue promptly.

Once the vulnerability is confirmed and patched, I will:
1. Acknowledge your contribution (unless you wish to remain anonymous).
2. Deploy the fix to the live system.
3. Update this policy if necessary.

---

## Security Considerations for This Project

- **API Key Protection**: This application uses API keys to authenticate requests to the FastAPI backend. All keys should be stored as **environment variables** (e.g., `API_KEY`, `SLACK_BOT_TOKEN`). **Never** hardcode credentials in the source code.
- **Deployment Isolation**: The system is designed to run within a secure AWS EC2 environment with IAM roles and security groups. No sensitive data is stored or logged in plain text.
- **Clinical Decision Support**: This tool is intended for **decision-support purposes only**. It does **not** replace clinical judgment or provide medical advice. See the main [README](README.md) for the full disclaimer.
- **Data Privacy**: Patient data is not stored or persisted in this system. The model processes text inputs in real-time and returns predictions without retaining any identifying information.

---

## Best Practices for Users

If you are deploying this project, please follow these security best practices:

1. **Use Environment Variables**: Always use environment variables for sensitive values (tokens, keys, passwords).
2. **Keep Dependencies Updated**: Regularly update `requirements.txt` to patch known vulnerabilities in dependencies.
3. **Limit Access**: Use AWS Security Groups to restrict access to your EC2 instance (e.g., only allow traffic on port 80/443 from trusted IPs).
4. **Monitor Logs**: Regularly check Docker logs for unusual activity.

---

## Responsible Disclosure Policy

I follow a responsible disclosure process. If you report a vulnerability in good faith, I will:
- Investigate and confirm the issue.
- Not take legal action against you.
- Credit you for the discovery (if you wish).

---

**Last Updated:** July 8, 2026
