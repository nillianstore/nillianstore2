# Social Media Bot Setup Guide

This guide will help you configure the Social Media Automation Bot workflow.

## Required GitHub Secrets

The workflow requires the following secrets to be set up in your GitHub repository. Add them by going to:
**Settings → Secrets and variables → Actions → New repository secret**

### Required Secrets:

| Secret Name | Description | Example |
|---|---|---|
| `GROQ_API_KEY` | API key from Groq for content generation | `gsk_xxxxxxxxxxxxx` |
| `META_ACCESS_TOKEN` | Facebook/Instagram access token | `EAAxxxxxxxxxxxx` |
| `FB_PAGE_ID` | Your Facebook Page ID | `123456789` |
| `IG_USER_ID` | Your Instagram Business Account ID | `987654321` |

### Optional:
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions, used for syncing logs back to the repository

## How to Get Each Secret:

### 1. **GROQ_API_KEY**
- Visit [https://console.groq.com](https://console.groq.com)
- Sign up or login to your Groq account
- Navigate to API Keys section
- Create a new API key and copy it

### 2. **META_ACCESS_TOKEN**
- Go to [https://developers.facebook.com](https://developers.facebook.com)
- Create an app or use existing one
- Generate a long-lived page access token
- Ensure your token has these permissions:
  - `pages_manage_metadata`
  - `pages_read_engagement`
  - `instagram_basic`
  - `instagram_content_publishing`

### 3. **FB_PAGE_ID**
- Go to your Facebook Page
- Look at the page URL or use Facebook Graph API to get your page ID
- Example format: `123456789123456`

### 4. **IG_USER_ID**
- Go to your Instagram Business Account settings
- Find your Business Account ID in the settings
- Example format: `987654321987654321`

## Workflow Behavior

The workflow runs automatically every 8 hours (configured via cron: `0 */8 * * *`) or manually via GitHub Actions.

### On Success:
- ✓ Selects a random product from `/shop/` directory
- ✓ Generates engaging social media content using Groq AI
- ✓ Posts to both Instagram and Facebook
- ✓ Logs the posted product ID to `social_log.json`
- ✓ Syncs the log back to the repository

### On Failure:
- The workflow will retry up to 3 times with different products
- Detailed error messages are printed to the workflow logs
- If all attempts fail, the workflow exits with status code 1

## Workflow Logs

To check workflow logs:
1. Go to your repository
2. Click on **Actions** tab
3. Click on **Social Media Automation Bot**
4. Select the most recent run
5. Click on the **post** job to view detailed logs

## Troubleshooting

### "Missing required secrets" error
- Verify all 4 secrets are added to your repository
- Check spelling matches exactly: `GROQ_API_KEY`, `META_ACCESS_TOKEN`, `FB_PAGE_ID`, `IG_USER_ID`
- Ensure secrets are not empty

### "Failed to post to social media" error
- Check that your API tokens are valid and not expired
- Verify your Facebook/Instagram permissions are correct
- Check the API response in workflow logs for specific errors

### No posts happening
- The workflow only runs every 8 hours by default
- You can manually trigger it from Actions → Social Media Automation Bot → Run workflow
- Check that your `/shop/` directory contains markdown files with product data

## Manual Trigger

To run the bot manually:
1. Go to **Actions** tab in your repository
2. Select **Social Media Automation Bot**
3. Click **Run workflow**
4. Select the branch (main) and click **Run workflow**

## Notes

- The bot maintains a history of recently posted products in `social_log.json` to avoid repetition
- Each workflow run posts one product to both Instagram and Facebook
- The bot uses Groq's Llama 3.3 model for content generation
- All posts include product link and auto-generated hashtags
