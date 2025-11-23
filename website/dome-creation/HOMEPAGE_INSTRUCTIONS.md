HomePage image placement

The React app `dome-creation` expects the `HomePage.png` image to be available from the app's public root so it's served at `/HomePage.png`.

To make the image load correctly:

1. Copy `HomePage.png` from the repository root into the React app `public` folder:

   - Source: `../HomePage.png` (repo root)
   - Destination: `public/HomePage.png` inside `website/dome-creation`

   Example (PowerShell):

   ```powershell
   cd "c:\Users\redrupm\OneDrive - Milwaukee School of Engineering\Desktop\ai\hacksgiving-2025-dome-inators\website\dome-creation"
   copy-item "..\..\HomePage.png" -Destination .\public\HomePage.png
   ```

2. Restart the dev server if it's running.

Notes:
- The `HomePage.jsx` component uses `src="/HomePage.png"` so the image must be placed at the public root.
- If you prefer to store the image under `public/images/HomePage.png`, update the component to use `/images/HomePage.png`.
