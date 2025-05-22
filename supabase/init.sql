-- ─────────────────────────────────────────────
-- 1. Base Tables
-- ─────────────────────────────────────────────
CREATE TABLE public.test_forms (
    id   BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE public.sections (
    id        BIGSERIAL PRIMARY KEY,
    test_id   BIGINT  NOT NULL REFERENCES public.test_forms(id) ON DELETE CASCADE,
    label     TEXT    NOT NULL,          -- Reading / Listening …
    order_no  INT     NOT NULL,
    CONSTRAINT sections_test_order_unique UNIQUE (test_id, order_no)
);

CREATE TABLE public.parts (
    id               BIGSERIAL PRIMARY KEY,
    section_id       BIGINT  NOT NULL REFERENCES public.sections(id) ON DELETE CASCADE,
    label            TEXT    NOT NULL,   -- Part 5, Part 6…
    question_format  TEXT    NOT NULL,   -- short_blank / long_blank …
    order_no         INT     NOT NULL,
    CONSTRAINT parts_section_order_unique UNIQUE (section_id, order_no)
);

-- ─────────────────────────────────────────────
-- 2. Passage-sets  &  Passages
-- ─────────────────────────────────────────────
CREATE TABLE public.passage_sets (
    id              BIGSERIAL PRIMARY KEY,
    part_id         BIGINT     NOT NULL REFERENCES public.parts(id) ON DELETE CASCADE,
    order_no        INT        NOT NULL,
    question_range  INT4RANGE  NOT NULL, -- [191,196) など
    title           TEXT,
    metadata        JSONB,
    CONSTRAINT passage_sets_part_order_unique UNIQUE (part_id, order_no)
);

CREATE TABLE public.passages (
    id               BIGSERIAL PRIMARY KEY,
    passage_set_id   BIGINT  NOT NULL REFERENCES public.passage_sets(id) ON DELETE CASCADE,
    order_no         INT     NOT NULL,
    body             TEXT    NOT NULL,
    metadata         JSONB,
    CONSTRAINT passages_set_order_unique UNIQUE (passage_set_id, order_no)
);

-- ─────────────────────────────────────────────
-- 3. Questions  &  Choices
-- ─────────────────────────────────────────────
CREATE TABLE public.questions (
    id                BIGSERIAL PRIMARY KEY,
    passage_set_id    BIGINT NOT NULL REFERENCES public.passage_sets(id) ON DELETE CASCADE,
    part_id           BIGINT NOT NULL REFERENCES public.parts(id)         ON DELETE CASCADE,
    number            INT    NOT NULL,  -- 101, 132 …
    blank_index       INT,              -- NULL = “空所なし”
    stem              TEXT   NOT NULL,
    answer_explanation TEXT,
    difficulty        TEXT,
    attributes        JSONB,
    CONSTRAINT questions_part_number_unique UNIQUE (part_id, number)
);

CREATE TABLE public.choices (
    id           BIGSERIAL PRIMARY KEY,
    question_id  BIGINT  NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    label        TEXT    NOT NULL,    -- A / B / C / D
    content      TEXT    NOT NULL,
    is_correct   BOOLEAN NOT NULL,
    CONSTRAINT choices_question_label_unique UNIQUE (question_id, label)
);

-- ─────────────────────────────────────────────
-- 4. Tags  &  Intermediate Tables
-- ─────────────────────────────────────────────
CREATE TABLE public.tags (
    id      BIGSERIAL PRIMARY KEY,
    level1  TEXT NOT NULL,
    level2  TEXT,
    level3  TEXT
);

CREATE TABLE public.question_tags (
    question_id BIGINT NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    tag_id      BIGINT NOT NULL REFERENCES public.tags(id)      ON DELETE CASCADE,
    PRIMARY KEY (question_id, tag_id)
);

-- ─────────────────────────────────────────────
-- 5. Indexes for Search & JOIN Optimization
-- ─────────────────────────────────────────────
CREATE INDEX idx_questions_passage_set  ON public.questions (passage_set_id);
CREATE INDEX idx_passages_set           ON public.passages  (passage_set_id);
CREATE INDEX idx_parts_section          ON public.parts     (section_id);
CREATE INDEX idx_sections_test          ON public.sections  (test_id);
