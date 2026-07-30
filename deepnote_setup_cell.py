# =============================================================
# PASTE THIS INTO A SINGLE DEEPNOTE CODE CELL AND RUN IT ONCE.
# It fixes the "cannot import name 'genai' from 'google'" error
# and prepares everything needed to launch the Streamlit app.
# =============================================================

# --- Step 1: Force-clean and reinstall the correct SDK -------
# Deepnote's base image sometimes ships a partial "google"
# namespace package (from google-cloud-* libs) that shadows
# google-genai. A normal `pip install` doesn't always fix this,
# so we uninstall anything conflicting and force a clean install.
!pip uninstall -y google-generativeai google-genai -q
!pip install --upgrade --force-reinstall --no-cache-dir google-genai streamlit -q

print("✅ Packages reinstalled. You MUST restart the kernel now")
print("   (Deepnote menu: Kernel -> Restart) before running the next cell,")
print("   otherwise Python will still see the old broken import.")
