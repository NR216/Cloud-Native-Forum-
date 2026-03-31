BEGIN;

-- Demo users for seeded forum content.
-- Shared demo password for these seeded non-admin accounts: ForumDemo!2026
INSERT INTO users (username, password, role, created_at) VALUES
    ('alice_forum', 'scrypt:32768:8:1$VuDSTnZndjTRugu3$ac4432083c3f7cacf20fc59ea6f20a4695ecb49d2c3dffb1075da159bc74d2da91af4520e8bddb4476083d25b8e6fe266cc1a9b43ffcad576b31b3a87fdf8507', 'user', '2026-03-30 18:00:00'),
    ('bob_forum', 'scrypt:32768:8:1$ynP2pM1LDBS9iQQt$c5d167b1b0a281b2673968996e5e0b3898e0f9a5d333322fd98b604acfeb896d39621caad7c0f5f29fdbbeafb5d8bd3191e9627b9ead039bb062ebf539154e91', 'user', '2026-03-30 18:02:00'),
    ('charlie_forum', 'scrypt:32768:8:1$tuSy5QPtdum2XAYs$0f43ce689b29caa1a7373ff5566b47c97fbea090ff772a6f8449af6a642c541e1c4d7c0ce8431b701b541603ed7022253939261509b220bd2a9b66a0ab32a5de', 'user', '2026-03-30 18:04:00'),
    ('mia_studyhall', 'scrypt:32768:8:1$KPRYtuPniDZ5gyhQ$f27d540b0ad893c293a1adf8ad593dee539e5dab9861a5311e27042d09373a077d7f65e6560d8222548546e22600d1c4fdebbd1b64a1e6fdda3ef117067d047b', 'user', '2026-03-30 18:06:00'),
    ('westend_reader', 'scrypt:32768:8:1$YtELnhZFIAuU9x8t$11ea4f068fbff5612b5cea198f71ba7c1f7e22c0aaf532d12eac8dca4c56a17e9107290685776405a31010efbeb2c2d6cab173b156cf1dc6c9a0ff1bb9107961', 'user', '2026-03-30 18:08:00'),
    ('transit_nightowl', 'scrypt:32768:8:1$mwXRgV3rntaHNs5f$b8b1f6c1c7fd59b6a3809b606170ea03d7d9c1729290a6facdf24c12e3c0b40c2a806738556758669cfacdde64ffdf357cc02f1552063f4e76a97b6a3d310897', 'user', '2026-03-30 18:10:00'),
    ('espresso_static', 'scrypt:32768:8:1$pI3huLClaHwFuxP1$ab226d974f57cc45ad4ef2efc347efd12565b0bb89cc203d0a5c56ef9b9072ccaa32956b2d7a3f684baad3d9ee4c3b917f1a29db7f2fcbf2fcd5bd7f5a570ae2', 'user', '2026-03-30 18:12:00'),
    ('labhumor', 'scrypt:32768:8:1$TQAHkfdWwmbvVevB$69ee292a10affcb0e801f1694aa30dddf807700c0e388d17bfd8f4d83f5349b09c25c399c487de1ce9b57010e33b44a1aa68d8b4daeaaf8b834410dab852fba3', 'user', '2026-03-30 18:14:00')
ON CONFLICT (username) DO NOTHING;

INSERT INTO posts (title, content, image_url, is_anonymous, author_id, created_at)
SELECT
    'Why does every quantum mechanics explanation turn into philosophy by page three?',
    'I only wanted a clean explanation of wavefunctions and measurement, but by the third page every book suddenly sounds like it is negotiating with reality itself. If anyone has a recommendation that stays mathematically clear without drifting into metaphysics too early, please share it.',
    '/static/demo/quantum-whiteboard.svg',
    FALSE,
    u.id,
    '2026-03-30 19:00:00'
FROM users u
WHERE u.username = 'mia_studyhall'
  AND NOT EXISTS (
      SELECT 1 FROM posts
      WHERE title = 'Why does every quantum mechanics explanation turn into philosophy by page three?'
  );

INSERT INTO posts (title, content, image_url, is_anonymous, author_id, created_at)
SELECT
    'NMR question: how much should I trust the tiny shoulder peak?',
    'I have been looking at one spectrum for long enough that I am no longer sure whether the small shoulder peak is meaningful chemistry or just me over-reading noise. Curious how other people decide when to stop chasing phantom structure and move on.',
    '/static/demo/chemistry-spectrum.svg',
    FALSE,
    u.id,
    '2026-03-30 19:12:00'
FROM users u
WHERE u.username = 'westend_reader'
  AND NOT EXISTS (
      SELECT 1 FROM posts
      WHERE title = 'NMR question: how much should I trust the tiny shoulder peak?'
  );

INSERT INTO posts (title, content, image_url, is_anonymous, author_id, created_at)
SELECT
    'Anonymous: explaining time complexity out loud is harder than writing the code',
    'I can implement the algorithm, I can usually pass the assignment, and I can even optimize the obvious bottlenecks. But the second someone asks me to explain the runtime in complete sentences, my brain suddenly forgets what O(n log n) means. Anyone else have this problem?',
    '/static/demo/cs-complexity-board.svg',
    TRUE,
    u.id,
    '2026-03-30 19:25:00'
FROM users u
WHERE u.username = 'charlie_forum'
  AND NOT EXISTS (
      SELECT 1 FROM posts
      WHERE title = 'Anonymous: explaining time complexity out loud is harder than writing the code'
  );

INSERT INTO posts (title, content, image_url, is_anonymous, author_id, created_at)
SELECT
    'Photo of the board after office hours',
    'Posting this because the board looked almost poetic after everyone left. Half derivation, half crisis, half coffee plan. I am pretty sure that adds up to more than one whole night, which feels accurate for this semester.',
    '/static/demo/lab-notes-desk.svg',
    FALSE,
    u.id,
    '2026-03-30 19:40:00'
FROM users u
WHERE u.username = 'alice_forum'
  AND NOT EXISTS (
      SELECT 1 FROM posts
      WHERE title = 'Photo of the board after office hours'
  );

INSERT INTO posts (title, content, image_url, is_anonymous, author_id, created_at)
SELECT
    'Department coffee tastes peer reviewed and still rejected',
    'Every year I think the coffee cannot get any more severe, and every year the department somehow finds a darker roast and a sadder machine. Please contribute your lab survival beverages so the rest of us can make better choices before 9 a.m. seminar.',
    '/static/demo/lab-notes-desk.svg',
    FALSE,
    u.id,
    '2026-03-30 19:52:00'
FROM users u
WHERE u.username = 'espresso_static'
  AND NOT EXISTS (
      SELECT 1 FROM posts
      WHERE title = 'Department coffee tastes peer reviewed and still rejected'
  );

INSERT INTO posts (title, content, image_url, is_anonymous, author_id, created_at)
SELECT
    'What makes a good project demo when half the work is infrastructure?',
    'Our project works, but a lot of the hardest work was not in the UI. It was deployment, monitoring, debugging containers, and making the stateful pieces behave. How do you present that in a short demo without making the app itself look small?',
    '/static/demo/cs-complexity-board.svg',
    FALSE,
    u.id,
    '2026-03-30 20:05:00'
FROM users u
WHERE u.username = 'bob_forum'
  AND NOT EXISTS (
      SELECT 1 FROM posts
      WHERE title = 'What makes a good project demo when half the work is infrastructure?'
  );

INSERT INTO posts (title, content, image_url, is_anonymous, author_id, created_at)
SELECT
    'Anonymous: does anyone become productive only when the deadline is close enough to smell?',
    'I do not recommend this workflow, but apparently my concentration reaches its highest form only after I have already complained for six hours and rearranged the desk twice. Looking for honest strategies, or at least solidarity.',
    '/static/demo/quantum-whiteboard.svg',
    TRUE,
    u.id,
    '2026-03-30 20:18:00'
FROM users u
WHERE u.username = 'transit_nightowl'
  AND NOT EXISTS (
      SELECT 1 FROM posts
      WHERE title = 'Anonymous: does anyone become productive only when the deadline is close enough to smell?'
  );

INSERT INTO posts (title, content, image_url, is_anonymous, author_id, created_at)
SELECT
    'Small campus joke collection for people stuck in the lab tonight',
    'I will start. The chemist said the reaction was under control, which was brave wording for a flask wearing three clamps and an ice bath like body armor. Please add your best course-safe lab or coding jokes below.',
    '/static/demo/chemistry-spectrum.svg',
    FALSE,
    u.id,
    '2026-03-30 20:30:00'
FROM users u
WHERE u.username = 'labhumor'
  AND NOT EXISTS (
      SELECT 1 FROM posts
      WHERE title = 'Small campus joke collection for people stuck in the lab tonight'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'For quantum, Griffiths is still the least theatrical starting point for me. I only open the more philosophical texts after I know the algebraic picture already makes sense.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 19:03:00'
FROM posts p, users u
WHERE p.title = 'Why does every quantum mechanics explanation turn into philosophy by page three?'
  AND u.username = 'bob_forum'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'For quantum, Griffiths is still the least theatrical starting point for me. I only open the more philosophical texts after I know the algebraic picture already makes sense.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'Same problem here. The moment a chapter starts asking what observation really means, I know I am about to lose twenty minutes and one page of useful notes.',
    TRUE,
    p.id,
    u.id,
    '2026-03-30 19:05:00'
FROM posts p, users u
WHERE p.title = 'Why does every quantum mechanics explanation turn into philosophy by page three?'
  AND u.username = 'transit_nightowl'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'Same problem here. The moment a chapter starts asking what observation really means, I know I am about to lose twenty minutes and one page of useful notes.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'If the shoulder peak does not behave consistently across repeats, I usually stop assigning it a dramatic backstory. Replication is kinder than imagination.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 19:16:00'
FROM posts p, users u
WHERE p.title = 'NMR question: how much should I trust the tiny shoulder peak?'
  AND u.username = 'alice_forum'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'If the shoulder peak does not behave consistently across repeats, I usually stop assigning it a dramatic backstory. Replication is kinder than imagination.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'My supervisor calls those mystery bumps tuition. Painful, but memorable.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 19:18:00'
FROM posts p, users u
WHERE p.title = 'NMR question: how much should I trust the tiny shoulder peak?'
  AND u.username = 'labhumor'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'My supervisor calls those mystery bumps tuition. Painful, but memorable.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'You are not alone. I can derive it on paper, but speaking it aloud makes me sound like I met Big-O notation five minutes ago.',
    TRUE,
    p.id,
    u.id,
    '2026-03-30 19:28:00'
FROM posts p, users u
WHERE p.title = 'Anonymous: explaining time complexity out loud is harder than writing the code'
  AND u.username = 'mia_studyhall'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'You are not alone. I can derive it on paper, but speaking it aloud makes me sound like I met Big-O notation five minutes ago.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'Practicing with one concrete input size helps. I explain what happens for ten items, then scale the pattern up from there.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 19:31:00'
FROM posts p, users u
WHERE p.title = 'Anonymous: explaining time complexity out loud is harder than writing the code'
  AND u.username = 'westend_reader'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'Practicing with one concrete input size helps. I explain what happens for ten items, then scale the pattern up from there.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'This board has exactly the energy of people who promised they would leave at six and then noticed one more thing worth fixing.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 19:45:00'
FROM posts p, users u
WHERE p.title = 'Photo of the board after office hours'
  AND u.username = 'charlie_forum'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'This board has exactly the energy of people who promised they would leave at six and then noticed one more thing worth fixing.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'The dangerous part is that from far away it looks organized enough to invite another question.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 19:47:00'
FROM posts p, users u
WHERE p.title = 'Photo of the board after office hours'
  AND u.username = 'bob_forum'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'The dangerous part is that from far away it looks organized enough to invite another question.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'If the infrastructure work prevented the app from falling apart during demo, then it is demo-worthy. I would show one user-facing flow and then one dashboard or deployment detail that proves the hard part.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 20:09:00'
FROM posts p, users u
WHERE p.title = 'What makes a good project demo when half the work is infrastructure?'
  AND u.username = 'alice_forum'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'If the infrastructure work prevented the app from falling apart during demo, then it is demo-worthy. I would show one user-facing flow and then one dashboard or deployment detail that proves the hard part.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'A short before-and-after story helps: what failed early, what you instrumented, and what became reliable afterward.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 20:11:00'
FROM posts p, users u
WHERE p.title = 'What makes a good project demo when half the work is infrastructure?'
  AND u.username = 'westend_reader'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'A short before-and-after story helps: what failed early, what you instrumented, and what became reliable afterward.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'Solidarity. My study plan becomes dramatically more sophisticated exactly one hour before panic.',
    TRUE,
    p.id,
    u.id,
    '2026-03-30 20:21:00'
FROM posts p, users u
WHERE p.title = 'Anonymous: does anyone become productive only when the deadline is close enough to smell?'
  AND u.username = 'mia_studyhall'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'Solidarity. My study plan becomes dramatically more sophisticated exactly one hour before panic.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'I bribe myself with a timer and a better coffee than the department one. It is not noble, but it is reproducible.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 20:23:00'
FROM posts p, users u
WHERE p.title = 'Anonymous: does anyone become productive only when the deadline is close enough to smell?'
  AND u.username = 'espresso_static'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'I bribe myself with a timer and a better coffee than the department one. It is not noble, but it is reproducible.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'Computer science version: the code compiles after I threaten it with sleep deprivation and bad snacks.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 20:33:00'
FROM posts p, users u
WHERE p.title = 'Small campus joke collection for people stuck in the lab tonight'
  AND u.username = 'bob_forum'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'Computer science version: the code compiles after I threaten it with sleep deprivation and bad snacks.'
  );

INSERT INTO replies (content, is_anonymous, post_id, author_id, created_at)
SELECT
    'Physics version: we did not lose the minus sign, we merely redistributed it to a less observable location.',
    FALSE,
    p.id,
    u.id,
    '2026-03-30 20:35:00'
FROM posts p, users u
WHERE p.title = 'Small campus joke collection for people stuck in the lab tonight'
  AND u.username = 'mia_studyhall'
  AND NOT EXISTS (
      SELECT 1 FROM replies WHERE post_id = p.id AND content = 'Physics version: we did not lose the minus sign, we merely redistributed it to a less observable location.'
  );

INSERT INTO likes (post_id, user_id, created_at)
SELECT p.id, u.id, '2026-03-30 19:06:00'
FROM posts p, users u
WHERE p.title = 'Why does every quantum mechanics explanation turn into philosophy by page three?'
  AND u.username = 'alice_forum'
ON CONFLICT (post_id, user_id) DO NOTHING;

INSERT INTO likes (post_id, user_id, created_at)
SELECT p.id, u.id, '2026-03-30 19:07:00'
FROM posts p, users u
WHERE p.title = 'Why does every quantum mechanics explanation turn into philosophy by page three?'
  AND u.username = 'westend_reader'
ON CONFLICT (post_id, user_id) DO NOTHING;

INSERT INTO likes (post_id, user_id, created_at)
SELECT p.id, u.id, '2026-03-30 19:20:00'
FROM posts p, users u
WHERE p.title = 'NMR question: how much should I trust the tiny shoulder peak?'
  AND u.username = 'mia_studyhall'
ON CONFLICT (post_id, user_id) DO NOTHING;

INSERT INTO likes (post_id, user_id, created_at)
SELECT p.id, u.id, '2026-03-30 19:34:00'
FROM posts p, users u
WHERE p.title = 'Anonymous: explaining time complexity out loud is harder than writing the code'
  AND u.username = 'bob_forum'
ON CONFLICT (post_id, user_id) DO NOTHING;

INSERT INTO likes (post_id, user_id, created_at)
SELECT p.id, u.id, '2026-03-30 19:36:00'
FROM posts p, users u
WHERE p.title = 'Anonymous: explaining time complexity out loud is harder than writing the code'
  AND u.username = 'alice_forum'
ON CONFLICT (post_id, user_id) DO NOTHING;

INSERT INTO likes (post_id, user_id, created_at)
SELECT p.id, u.id, '2026-03-30 19:49:00'
FROM posts p, users u
WHERE p.title = 'Photo of the board after office hours'
  AND u.username = 'transit_nightowl'
ON CONFLICT (post_id, user_id) DO NOTHING;

INSERT INTO likes (post_id, user_id, created_at)
SELECT p.id, u.id, '2026-03-30 20:13:00'
FROM posts p, users u
WHERE p.title = 'What makes a good project demo when half the work is infrastructure?'
  AND u.username = 'charlie_forum'
ON CONFLICT (post_id, user_id) DO NOTHING;

INSERT INTO likes (post_id, user_id, created_at)
SELECT p.id, u.id, '2026-03-30 20:25:00'
FROM posts p, users u
WHERE p.title = 'Anonymous: does anyone become productive only when the deadline is close enough to smell?'
  AND u.username = 'westend_reader'
ON CONFLICT (post_id, user_id) DO NOTHING;

INSERT INTO likes (post_id, user_id, created_at)
SELECT p.id, u.id, '2026-03-30 20:37:00'
FROM posts p, users u
WHERE p.title = 'Small campus joke collection for people stuck in the lab tonight'
  AND u.username = 'espresso_static'
ON CONFLICT (post_id, user_id) DO NOTHING;

SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1), true);
SELECT setval('posts_id_seq', COALESCE((SELECT MAX(id) FROM posts), 1), true);
SELECT setval('replies_id_seq', COALESCE((SELECT MAX(id) FROM replies), 1), true);
SELECT setval('likes_id_seq', COALESCE((SELECT MAX(id) FROM likes), 1), true);
SELECT setval('reports_id_seq', COALESCE((SELECT MAX(id) FROM reports), 1), true);

COMMIT;
