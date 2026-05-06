---
name: Heritage & Ideology
colors:
  surface: '#f9f9f6'
  surface-dim: '#dadad7'
  surface-bright: '#f9f9f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f4f1'
  surface-container: '#eeeeeb'
  surface-container-high: '#e8e8e5'
  surface-container-highest: '#e2e3e0'
  on-surface: '#1a1c1b'
  on-surface-variant: '#5c403b'
  inverse-surface: '#2f312f'
  inverse-on-surface: '#f1f1ee'
  outline: '#906f6a'
  outline-variant: '#e5beb7'
  surface-tint: '#bb190e'
  primary: '#790000'
  on-primary: '#ffffff'
  primary-container: '#a50000'
  on-primary-container: '#ffaea1'
  inverse-primary: '#ffb4a8'
  secondary: '#705d00'
  on-secondary: '#ffffff'
  secondary-container: '#fcd400'
  on-secondary-container: '#6e5c00'
  tertiary: '#393939'
  on-tertiary: '#ffffff'
  tertiary-container: '#515050'
  on-tertiary-container: '#c4c2c2'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad4'
  primary-fixed-dim: '#ffb4a8'
  on-primary-fixed: '#410000'
  on-primary-fixed-variant: '#930000'
  secondary-fixed: '#ffe16d'
  secondary-fixed-dim: '#e9c400'
  on-secondary-fixed: '#221b00'
  on-secondary-fixed-variant: '#544600'
  tertiary-fixed: '#e5e2e1'
  tertiary-fixed-dim: '#c8c6c5'
  on-tertiary-fixed: '#1c1b1b'
  on-tertiary-fixed-variant: '#474746'
  background: '#f9f9f6'
  on-background: '#1a1c1b'
  surface-variant: '#e2e3e0'
typography:
  h1:
    fontFamily: Newsreader
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  h2:
    fontFamily: Newsreader
    fontSize: 36px
    fontWeight: '600'
    lineHeight: '1.3'
  h3:
    fontFamily: Newsreader
    fontSize: 28px
    fontWeight: '500'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.7'
  body-md:
    fontFamily: Be Vietnam Pro
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Be Vietnam Pro
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.1em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-max: 1200px
  gutter: 24px
  margin-mobile: 16px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style
The design system is engineered to evoke a sense of solemnity, historical weight, and institutional authority. It balances the ideological gravity of the Vietnamese Communist Party’s history with a modern, accessible educational interface. The brand personality is "The Venerable Educator": disciplined, clear, and deeply rooted in national heritage.

The style is **Modern Corporate with Tactile accents**. It utilizes high-quality whitespace and a structured grid to ensure information density remains readable. To avoid a purely digital feel, the system integrates subtle paper grain textures and faint "Dong Son" drum patterns or lotus motifs as background watermarks, grounding the modern UI in traditional Vietnamese aesthetics. The target audience includes students, researchers, and citizens seeking a definitive, official source of historical record.

## Colors
The palette is anchored by **Deep Crimson Red**, symbolizing revolution and the national flag, used for primary actions, headers, and key branding moments. **Gold** is reserved for high-value accents, highlights, and decorative flourishes like line separators or icons, ensuring it feels prestigious rather than gaudy.

The background uses a "Paper White" (#FDFDFB) rather than a pure digital white to reduce eye strain and enhance the tactile feel. **Light Grey** (#E5E5E1) is used for secondary containers and section backgrounds to create subtle visual hierarchy. Text is set in a near-black Charcoal to ensure maximum legibility while maintaining a softer contrast than pure black.

## Typography
This design system employs a sophisticated pairing of **Newsreader** for headings and **Be Vietnam Pro** for body text. 

**Newsreader** provides the authoritative, literary feel necessary for historical documentation, echoing the typography of traditional journals and official proclamations. **Be Vietnam Pro** is selected for its exceptional support for Vietnamese diacritics and its modern, neutral character that ensures long-form educational content is easy to digest. Use serif headings for all editorial titles and sans-serif for navigation, labels, and instructional text.

## Layout & Spacing
The layout follows a **Fixed Grid** system centered on the page to emphasize stability and order. A 12-column grid is used for desktop (1200px max-width), allowing for flexible content ratios such as 8-columns for primary text and 4-columns for supplemental historical data.

Vertical rhythm is strictly maintained using a 4px baseline unit. Generous "stack-lg" spacing is used between major historical eras or sections to allow the content to breathe. Margins are wider than average to simulate the proportions of a printed book or a formal document.

## Elevation & Depth
To maintain a solemn and historical atmosphere, the design system avoids heavy shadows or neon glows. Instead, it uses **Tonal Layers** and **Low-Contrast Outlines**.

Depth is conveyed through subtle shifts in background color (e.g., a card being slightly lighter than the page background) and 1px borders in a muted gold or light grey. When elevation is necessary for interactive elements like modals or dropdowns, a very soft, diffused ambient shadow with a hint of red tint (#A50000 at 5% opacity) is used to create a "lifted paper" effect rather than a digital floating effect.

## Shapes
The shape language is primarily **Soft (0.25rem)**. This slight rounding takes the edge off the "brutalist" institutional feel while remaining disciplined. 

Avoid high-radius circles or "pill" shapes for buttons, as they feel too casual for the subject matter. Rectangular elements with very small corner radii suggest the edges of historical documents, plaques, and framed photographs. Interactive cards should use the `rounded-lg` (0.5rem) setting to distinguish them as clickable objects.

## Components
- **Interactive Timelines:** A vertical Gold line serves as the anchor. Nodes are Deep Crimson circles that expand on hover. Active dates use Newsreader Serif to emphasize the passage of time.
- **Structured Content Cards:** Cards use the light grey background with a 2px top border in Deep Crimson. Photography within cards should use a subtle sepia or high-contrast black-and-white filter to maintain tonal consistency.
- **Buttons:** Primary buttons are solid Deep Crimson with white Be Vietnam Pro text. Secondary buttons use a Gold 1px outline. All buttons use the 'Soft' (0.25rem) corner radius.
- **Navigation:** A clean, top-fixed bar with a subtle paper texture. Links use uppercase Be Vietnam Pro with a Gold underline effect on active states.
- **Fact Sheets/Sidebars:** Use a faint Vietnamese pattern watermark in the background of these containers to differentiate them from the main narrative flow.
- **Inputs & Forms:** Simple, clean borders that turn Deep Crimson on focus. Labels are always placed above the field in bold sans-serif.