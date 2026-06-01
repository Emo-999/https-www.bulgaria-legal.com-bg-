"""Apply the premium palette to the knowledge-freedom theme variables (best-effort;
customCssJs is the reliable layer). Maps brand palette across the color-* variables."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from cc_graphql import gql
import brand as B

# parameter -> value
V = {
    # main
    "color-main-background": B.PAPER, "color-main-borders": B.LINE,
    "color-main-text": B.TEXT, "color-main-secondary-text": B.MUTED,
    "color-main-meta-text": B.MUTED, "color-main-titles": B.INK,
    "color-main-highlight": B.CRIMSON, "color-main-icons": B.CRIMSON,
    # second surface
    "color-second-background": B.PAPER_2, "color-second-borders": B.LINE,
    "color-second-text": B.TEXT, "color-second-titles": B.INK,
    "color-second-highlight": B.CRIMSON, "color-second-image-box": B.PAPER,
    "color-second-button-background": B.CRIMSON, "color-second-button-borders": B.CRIMSON,
    "color-second-button-text": B.PAPER,
    "color-second-button-background-hover": B.CRIMSON_D, "color-second-button-borders-hover": B.CRIMSON_D,
    "color-second-button-text-hover": B.PAPER,
    "color-second-button-secondary-background": B.PAPER, "color-second-button-secondary-borders": B.INK,
    "color-second-button-secondary-text": B.INK,
    "color-second-button-secondary-background-hover": B.INK, "color-second-button-secondary-borders-hover": B.INK,
    "color-second-button-secondary-text-hover": B.PAPER,
    # header
    "color-header-background": B.PAPER, "color-header-borders": B.LINE,
    "color-header-text": B.INK, "color-header-secondary-text": B.MUTED,
    "color-header-icons": B.INK, "color-header-icons-hover": B.CRIMSON,
    "color-header-icons-bubble-background": B.CRIMSON, "color-header-icons-bubble-text": B.PAPER,
    # navigation
    "color-navigation-background": B.PAPER, "color-navigation-text": B.INK,
    "color-navigation-hover-background": B.PAPER, "color-navigation-hover-text": B.CRIMSON,
    # dropdowns
    "color-dropdowns-background": B.PAPER, "color-dropdowns-borders": B.LINE,
    "color-dropdowns-text": B.TEXT, "color-dropdowns-highlight": B.CRIMSON,
    "color-dropdowns-button-background": B.CRIMSON, "color-dropdowns-button-borders": B.CRIMSON,
    "color-dropdowns-button-text": B.PAPER,
    "color-dropdowns-button-background-hover": B.CRIMSON_D, "color-dropdowns-button-borders-hover": B.CRIMSON_D,
    "color-dropdowns-button-text-hover": B.PAPER,
    # footer (dark charcoal premium)
    "color-footer-background": B.INK, "color-footer-borders": "#2A2D34",
    "color-footer-text": "#C7C9CE", "color-footer-titles": B.PAPER, "color-footer-highlight": B.GOLD,
    "color-footer-socials-background": B.INK, "color-footer-socials-icon": "#C7C9CE",
    "color-footer-socials-icon-background": B.INK_2, "color-footer-socials-icon-hover": B.GOLD,
    "color-footer-socials-icon-background-hover": B.INK_2,
    "color-footer-bottom-bar-background": "#101216", "color-footer-bottom-bar-text": "#8A8D94",
    "color-footer-bottom-bar-links": B.SLATE, "color-footer-bottom-bar-highlight": B.GOLD,
    # topbar (dark)
    "color-topbar-background": B.INK, "color-topbar-borders": B.INK,
    "color-topbar-text": "#E9E6E1", "color-topbar-icons": B.GOLD, "color-topbar-hovers": B.GOLD,
    # slider
    "color-slider-background": B.INK, "color-slider-text": B.PAPER, "color-slider-titles": B.PAPER,
    "color-slider-arrows": B.PAPER, "color-slider-dots": B.GOLD,
    "color-slider-button-background": B.CRIMSON,
}

variables = [{"parameter": k, "value": v} for k, v in V.items()]
print(f"Applying {len(variables)} theme variables...")
r = gql('mutation($input:UpdateThemeVariablesInput!){ updateThemeVariables(input:$input){ templateName } }',
        {"input": {"variables": variables}})
if r.get("errors"):
    print("  (theme vars returned errors — expected; customCssJs is the reliable layer)")
    print("  ", json.dumps(r["errors"], ensure_ascii=False)[:300])
else:
    print("  theme variables applied:", json.dumps(r.get("data"), ensure_ascii=False)[:200])

# Clear the leftover builder test design on home (page 2)
c = gql('mutation($pageId:ID!,$input:SaveBuilderDesignInput!){ savePageBuilderDesign(pageId:$pageId,input:$input){ id } }',
        {"pageId": "2", "input": {"design": {"rows": []}, "publish": True}})
print("cleared home builder test design:", "ok" if not c.get("errors") else c.get("errors"))
