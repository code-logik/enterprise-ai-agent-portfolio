# AI Flashcard Deck Generation Instructions

## 1. Purpose

Use these instructions whenever the user asks AI to create a new flashcard deck for the AI Certification portfolio. Produce a weekly JSON data file that works with the existing Tkinter application, `flashcards.py`. Build the cards from the learning material or knowledge check supplied for that specific week.

**Repository rule:** The user alone updates GitHub. Do not create commits, push changes, open pull requests, or modify a connected repository on the user's behalf. Provide the finished deck file for the user to review and add themselves.

## 2. Existing application and authoritative files

The established portfolio layout is:

```text
enterprise-ai-agent-portfolio/
└── python-labs/
    └── study-tools/
        └── flashcards/
            ├── flashcards.py
            ├── AI-DECK-GENERATION-INSTRUCTIONS.md
            └── decks/
                ├── week_02.json
                ├── week_03.json
                └── week_template.json
```

Treat the current `flashcards.py`, the existing `week_02.json`, and `week_template.json` as the authoritative compatibility references when they are provided. The Python application looks for files in the `decks` folder next to `flashcards.py` using `week_[0-9][0-9].json`. It loads the decks when the application starts. `week_template.json` is a template, not a study deck.

**Scope:** A request for a new deck means create one new `week_XX.json` file. Do not change `flashcards.py`, the template, existing decks, folder structure, or other project files unless the user explicitly asks. Do not create a separate Python script for each week.

## 3. Information required for a new deck

Identify the requested week number, topic or theme, and the learning material to cover. Use material supplied in the current request, such as a weekly knowledge check, completed module notes, or other uploaded sources. Follow that material's terminology and scope. If the user asks for outside research or expanded coverage, distinguish additional material from the provided learning content.

Do not invent a module's contents, unseen document sections, completion status, exam objectives, or answers. If the week, theme, or source material is essential but missing, ask for only that missing information. Do not quietly substitute generic content for a requested source-based deck.

## 4. File name and location

Create exactly one file per requested week, named `week_XX.json` with a zero-padded **two-digit week number**. Examples: Week 3 becomes `week_03.json`; Week 12 becomes `week_12.json`; Week 26 becomes `week_26.json`.

Its intended destination within the portfolio is:

```text
python-labs/study-tools/flashcards/decks/week_XX.json
```

Do not overwrite an existing week file without the user's explicit request. If a replacement is requested, preserve the same file name and provide the revised file for the user to install.

## 5. Required JSON schema

Follow the existing data structure exactly:

```json
{
  "week": 3,
  "title": "Actual theme or title for Week 3",
  "cards": [
    {
      "category": "Concept category",
      "question": "What is the question?",
      "answer": "A concise, accurate answer."
    }
  ]
}
```

- The root must be a JSON object with `week`, `title`, and `cards`.
- `week` must be an integer matching the requested week and file name.
- `title` must be a meaningful, nonempty string describing that week's material.
- `cards` must be a nonempty JSON array.
- Every entry in `cards` must be an object with nonempty string values for `category`, `question`, and `answer`.
- Use only those fields unless the user explicitly requests an application change to support others. Do not add fields such as `id`, `front`, `back`, `correct_answer`, `difficulty`, `source`, `tags`, or `options` to the exported cards.
- Output valid JSON: double-quoted keys and strings, commas only between elements, no comments, no Markdown fences inside the file, and no trailing commas.
- Save the file as UTF-8 text.

## 6. Card-writing standards

1. Cover the important terms, definitions, processes, distinctions, and practical implications actually present in the supplied weekly material. Do not add filler to meet a quota.
2. Unless the user specifies a different count, target **10 cards** when the material supports that many. Use fewer if the source is too limited; use more only when needed for meaningful coverage or when requested.
3. Make each question self-contained and answerable without seeing another card. Aim for one main learning objective per card.
4. Make answers precise, concise, and suitable for recall. Include an example when it directly clarifies the concept, but avoid lengthy paragraphs that will be hard to read on the visual card.
5. Use consistent, specific categories such as `NLP`, `Speech`, `Retrieval`, or `Agents` where those categories match the week's content. Categories appear on the visual card.
6. Include comparison and application questions when supported by the learning material. Distinguish related concepts accurately rather than implying that one approach is universally better.
7. Do not invent knowledge-check answers or cite a document section that was not supplied. When material is ambiguous, preserve the stated distinction or flag the ambiguity for the user instead of guessing.
8. Avoid duplicate or near-duplicate questions, trick wording, unexplained abbreviations, and questions that depend on the cards appearing in a particular order. The app can shuffle cards and combine all weeks.
9. Each card must work in a self-rated front/back review flow. Do not create multiple-choice or fill-in-the-blank data formats the application does not support.

## 7. Compatibility and quality checks

Before delivering the file, verify all of the following:

- The file name matches `week_XX.json` and the `week` value.
- The JSON parses successfully, and the root, `cards`, and all card fields have the expected types.
- Each card has meaningful, nonblank `category`, `question`, and `answer` strings.
- All questions and answers are supported by the supplied material or explicitly requested outside sources.
- No existing Python code, decks, or template files were changed.
- The title and categories will be understandable when displayed in the deck selector and on the visual card.

If a local Python environment is available, run this JSON syntax check against the produced file:

```powershell
python -m json.tool .\week_03.json
```

Substitute the actual file name and its actual location. This confirms JSON syntax only, not factual accuracy or the complete schema. Validate the schema separately. You may test with the current application when a graphical desktop is available; do not claim the GUI was tested unless it was actually run.

The application discovers weekly decks on startup. If a new JSON file is added while the visual app is already running, close and reopen the app to see the new deck.

## 8. Deliverables for every new-deck request

Provide:

1. The completed `week_XX.json` file, with a download link when a file can be created.
2. A brief summary naming the week, title, and number of cards, and the source material used.
3. Its destination: `python-labs/study-tools/flashcards/decks/week_XX.json`.
4. Any content gaps or unverified facts that affected the deck, stated plainly.

Do not upload, commit, or push to GitHub. The user will review the deck and update their own repository.

## 9. Example request for the AI

> Using AI-DECK-GENERATION-INSTRUCTIONS.md and my Week 3 learning material, create the Week 3 visual flashcard deck. Follow the existing `week_02.json` format. Give me only the new `week_03.json` file and a short description. Do not modify `flashcards.py`, the template, any previous deck, or GitHub.
