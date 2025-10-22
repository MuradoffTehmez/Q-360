# Q360 Developer Guide

## TailwindCSS Build Process

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Setup
1. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

### Development
1. Watch for CSS changes:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

### Production Build
1. Build optimized CSS for production:
   ```bash
   npm run build
   # or
   yarn build
   ```

This will create an optimized `tailwind.css` file in the `static/css/` directory that will be used instead of the CDN version.

### CSS Configuration
- Source: `static_src/input.css`
- Output: `static/css/tailwind.css`
- Config: `tailwind.config.js`

## Django Static Files
After building the Tailwind CSS file, make sure to run:
```bash
python manage.py collectstatic
```

## Development Workflow
1. Make changes to templates
2. Update `static_src/input.css` if needed
3. Run `npm run dev` for development or `npm run build` for production
4. The built CSS will be automatically picked up by Django

## Important Notes
- During development, you can use the CDN version by uncommenting the script tag in `base.html`
- For production deployment, always use the locally built CSS file
- The production CSS file is optimized and minified with unused classes purged