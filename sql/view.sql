CREATE VIEW test_view AS
SELECT
    u.id AS user_id,
    u.username,
    d.fname,
    d.lname,
    d.phone,
    d.email,
    d.address,
    d.postalZip,
    d.city,
    d.country,
    d.registration_datetime,
    us.salt
FROM
    user u
JOIN
    details d ON u.id = d.user_id
JOIN
    userSalt us ON u.id = us.user_id;