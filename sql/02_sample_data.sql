
-- ============================================
-- 02: INSERT SAMPLE USERS
-- ============================================

INSERT INTO users (username, email)
VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com');


-- ============================================
-- INSERT SAMPLE CALCULATIONS
-- ============================================

-- Alice's calculations (user_id = 1)
INSERT INTO calculations (
    operation,
    operand_a,
    operand_b,
    result,
    user_id
)
VALUES
    ('addition', 10, 5, 15, 1),
    ('subtraction', 10, 4, 6, 1);

-- Bob's calculation (user_id = 2)
INSERT INTO calculations (
    operation,
    operand_a,
    operand_b,
    result,
    user_id
)
VALUES
    ('multiplication', 6, 7, 42, 2);
