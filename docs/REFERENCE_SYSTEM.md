# Reference System

The Career Coach has three knowledge layers:

1. Public generic references: `references/*.md`
2. Private or licensed local notes: `references.local/*.md`
3. Personal user context: `context/*.local.md`

This lets the coach answer cross-person general questions while still supporting personalized coaching when local context exists.

## Why This Matters

Without a reference layer, the coach is only a prompt wrapper around a user profile. With a reference layer, it can answer questions like:

- How should I prepare for a product interview?
- How do I decide whether to accept an offer?
- How do I build influence without formal authority?
- How do I turn project work into promotion evidence?

These questions can be answered generally first, then personalized with a user profile.

## Lenny Podcast Notes

Lenny's Podcast can be used as a reference source, but the public repo should not contain full transcripts, full episode notes, or long copyrighted summaries.

Recommended approach:

1. Maintain public source metadata and short, transformative principles in `references/`.
2. Keep detailed personal notes or licensed summaries in `references.local/`.
3. Organize notes by theme, not only by episode.
4. Require source URLs for every note.
5. Make the coach say when a claim is unsupported by the loaded notes.

## Suggested Lenny Digest Format

```markdown
# Lenny Digest Local

## Product Judgment

### Source: <episode title and URL>
- Principle:
- Use when:
- Watch out:

## Career Growth

### Source: <episode title and URL>
- Principle:
- Use when:
- Watch out:
```

## Cross-Individual Question Handling

The coach should classify every request:

| Request type | Behavior |
|---|---|
| General career question | Answer from references and domain knowledge |
| Role-specific but not personal | Ask for role/seniority only if missing |
| Personal decision | Ask for up to two diagnostic facts |
| Confidential work issue | Use local profile only; avoid committing details |

## Completeness

The generic public repo should provide the mechanism and starter references. A complete reference library requires one of:

- User-authored notes
- Licensed summaries
- Public source metadata plus short original principles
- A private local knowledge base

The code intentionally supports this through `references.local/`.

