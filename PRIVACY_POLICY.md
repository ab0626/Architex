# Architex Privacy Policy

## Overview

Architex is a developer tool designed to analyze codebases and generate system design diagrams. This privacy policy explains how we handle your data and protect your privacy.

## Data Collection and Processing

### What Data We Collect

**Code Analysis Data:**
- Source code files from your codebase
- File structure and dependencies
- Code elements (classes, functions, modules)
- Relationships between code components

**Configuration Data:**
- Privacy settings and preferences
- Analysis configuration options
- User consent records

**Usage Data:**
- Analysis metrics and statistics
- Error logs (if enabled)
- Performance metrics

### What We Do NOT Collect

- Personal identifying information
- API keys, passwords, or credentials
- Sensitive configuration files
- User behavior outside the tool
- Network traffic data

## Data Processing Principles

### Local-First Architecture

By default, Architex processes all data locally on your machine:
- No data is sent to external services unless explicitly enabled
- Analysis results are not stored unless you configure it
- All processing happens in your local environment

### Data Minimization

We follow the principle of data minimization:
- Only collect data necessary for analysis
- Automatically exclude sensitive file patterns
- Respect `.gitignore` patterns
- Provide granular control over data collection

### Consent-Based Processing

AI-powered features require explicit consent:
- Clear consent prompts before AI analysis
- Granular consent for different features
- Easy consent revocation
- Transparent data handling policies

## AI Features and External Services

### When AI Features Are Used

AI features are **disabled by default** and require explicit consent:
- Component labeling and categorization
- Code summarization and recommendations
- Service boundary detection

### Data Transmission for AI

When AI features are enabled:
- Code snippets are anonymized before transmission
- Only relevant code sections are sent
- No persistent storage of transmitted data
- Processing follows the AI service provider's privacy policy

### AI Service Providers

Currently supported AI providers:
- OpenAI (GPT models)
- Anthropic (Claude models)
- Local models (when available)

## Privacy Controls

### Configuration Options

You can control privacy through:
- CLI commands (`architex privacy`, `architex privacy-settings`)
- Configuration file (`config.yaml`)
- Environment variables
- Interactive consent prompts

### Key Privacy Settings

```yaml
privacy:
  data_handling:
    local_only: true              # Process locally only
    store_analyzed_code: false    # Don't persist code
    store_ai_responses: false     # Don't store AI responses
    clear_cache_on_exit: true     # Auto-cleanup
  
  ai_features:
    enabled: false                # AI disabled by default
    require_consent: true         # Require explicit consent
    anonymize_code_before_ai: true # Anonymize before AI
  
  file_watching:
    respect_gitignore: true       # Follow .gitignore
    exclude_sensitive_patterns:   # Skip sensitive files
      - "*.env"
      - "*.key"
      - "secrets.json"
```

## Data Storage and Retention

### Local Storage

Data may be stored locally in:
- `.architex_cache/` - Analysis cache (configurable)
- `~/.architex/` - Configuration and settings
- Temporary files during analysis

### Retention Policies

- Cache files: 24 hours by default (configurable)
- Log files: 7 days by default (configurable)
- Configuration: Until manually deleted
- Consent records: 1 year (configurable)

### Data Cleanup

Automatic cleanup features:
- Cache cleanup on exit (configurable)
- Automatic cleanup of old files
- Manual cleanup command (`architex cleanup`)

## User Rights and Control

### Your Rights

You have the right to:
- **Access**: View all data collected about your usage
- **Control**: Configure what data is collected and stored
- **Delete**: Remove all stored data at any time
- **Consent**: Grant or revoke consent for features
- **Export**: Export your privacy settings and data

### How to Exercise Your Rights

**View Privacy Settings:**
```bash
architex privacy
```

**Update Privacy Settings:**
```bash
architex privacy-settings --local-only --ai-enabled false
```

**Grant/Revoke Consent:**
```bash
architex consent ai_analysis --grant
architex consent file_watching --revoke
```

**Export Privacy Report:**
```bash
architex privacy-report --output privacy_report.json
```

**Clean Up Data:**
```bash
architex cleanup
```

## Security Measures

### Data Protection

- Local processing by default
- No network transmission unless explicitly enabled
- Anonymization of sensitive data
- Secure configuration storage

### File System Security

- Respects file system permissions
- Only reads files you specify
- Excludes sensitive patterns automatically
- Follows `.gitignore` patterns

### Network Security

- Local WebSocket server (configurable)
- No external connections by default
- Secure communication when enabled
- Authentication for web interface

## Third-Party Services

### AI Service Providers

When using AI features, data is processed by:
- **OpenAI**: [OpenAI Privacy Policy](https://openai.com/privacy)
- **Anthropic**: [Anthropic Privacy Policy](https://www.anthropic.com/privacy)
- **Local Models**: No external transmission

### Data Sharing

We do not share your data with third parties except:
- AI service providers (with your consent)
- When required by law
- With your explicit permission

## Compliance

### GDPR Compliance

For EU users, we comply with GDPR:
- Right to access, rectification, and erasure
- Right to data portability
- Right to restrict processing
- Right to object to processing
- Consent management

### CCPA Compliance

For California users, we comply with CCPA:
- Right to know what data is collected
- Right to delete personal information
- Right to opt-out of data sharing
- Right to non-discrimination

## Children's Privacy

Architex is not intended for use by children under 13. We do not knowingly collect personal information from children under 13.

## Changes to This Policy

We may update this privacy policy from time to time. Changes will be:
- Posted on this page
- Communicated through release notes
- Available in the tool's documentation

## Contact Information

For privacy-related questions or concerns:
- Create an issue on our GitHub repository
- Review the privacy documentation
- Use the built-in privacy commands

## Data Breach Response

In the event of a data breach:
- We will notify affected users promptly
- Provide details about the breach
- Outline steps to protect your data
- Work to prevent future breaches

## Best Practices

### For Maximum Privacy

1. **Use local-only mode:**
   ```bash
   architex privacy-settings --local-only
   ```

2. **Disable AI features:**
   ```bash
   architex privacy-settings --ai-enabled false
   ```

3. **Enable automatic cleanup:**
   ```bash
   architex privacy-settings --clear-cache
   ```

4. **Review sensitive patterns:**
   ```bash
   architex privacy
   ```

5. **Regular cleanup:**
   ```bash
   architex cleanup
   ```

### For Sensitive Codebases

- Use local AI models when available
- Review all configuration settings
- Test with a small subset first
- Monitor what data is being processed

---

**Last Updated:** December 2024  
**Version:** 1.0  
**Effective Date:** December 2024
