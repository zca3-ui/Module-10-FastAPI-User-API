
-- ============================================
-- 03: SELECT ALL USERS
-- ============================================

SELECT * FROM users;


-- ============================================
-- SELECT ALL CALCULATIONS
-- ============================================

SELECT * FROM calculations;


-- ============================================
-- JOIN CALCULATIONS WITH USERS
-- ============================================

SELECT
    c.id AS calculation_id,
    u.username,
    c.operation,
    c.operand_a,
    c.operand_b,
    c.result,
    c.timestamp
FROM calculations c
JOIN users u
    ON c.user_id = u.id;


-- ============================================
-- UPDATE CALCULATION ID 1
-- ============================================

UPDATE calculations
SET result = 6
WHERE id = 1;


-- Verify the update
SELECT * FROM calculations
WHERE id = 1;


-- ============================================
-- DELETE CALCULATION ID 2
-- ============================================

DELETE FROM calculations
WHERE id = 2;


-- Verify the deletion
SELECT * FROM calculations;
