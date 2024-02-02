CREATE VIEW test_view AS
SELECT
    u.id AS user_id,
    u.username as username,
    d.fname as first_name,
    d.lname as last_name,
    d.phone as phone,
    d.email as email,
    d.address as address,
    d.postalZip as post_code,
    d.city as city,
    d.country as country,
    d.registration_datetime as data,
    us.salt as salt
    LENGTH(us.salt) as salt_len
FROM
    user u
JOIN
    details d ON u.id = d.user_id
JOIN
    userSalt us ON u.id = us.user_id;