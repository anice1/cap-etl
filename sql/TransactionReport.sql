WITH all_transactions AS (
        SELECT
            trx.from_country_id,
            trx.to_country_id,
            trx.payout_id,
            act.bank_id,
            trx.account_id,
            trx.reference,
            trx.status,
            trx.completed_at,
            act.account_name,
            act.bank_location,
            act.account_number,
            trx.send_amount,
            pro.othernames,
            pro.dob,
            pro.address_line_1,
            pro.suburb,
            state.name AS state_name,
            pro.postcode,
            country.name AS country_name,
            pro.mobile_phone,
            pro.occupation,
            pro.member_id,
            idt.name idtype_name,
            pro.idnumber,
            idt.issuer,
            trx.received_amount,
            trx.comment,
            trx.payin,
            pyts.name AS payout_name,
            trx.created_at
        FROM transactions trx
            JOIN accounts act ON act.id = trx.account_id
            JOIN users ON users.id = trx.user_id
            JOIN profiles pro ON pro.id = users.profile_id
            JOIN states state ON state.id = pro.state_id
            JOIN countries country ON country.id = pro.country_id
            JOIN idtypes idt ON idt.id = pro.idtype_id
            JOIN payouts pyts ON pyts.id = trx.payout_id
        WHERE
            (trx.created_at BETWEEN :from_param AND :to_param) AND
            (trx.payin = :payin_param) AND
            (trx.status = :status_param)

        ORDER BY
            created_at DESC
    ),
    bank_and_beneficiary_info AS (
        SELECT
            trx.*,
            banks.name AS bank_name,
            CONCAT(
                ben.first_name,
                ' ',
                ben.last_name
            ) AS ben_fullname,
            ben.address AS ben_address,
            ben.phone_no AS ben_phone,
            country.name AS ben_country
        FROM
            all_transactions trx
            JOIN banks ON banks.id = trx.bank_id
            JOIN beneficiaries ben ON trx.account_id = ben.id
            JOIN countries country ON country.id = ben.country_id
    ),
    get_sent_currency_code AS (
        SELECT
            bank_and_ben.*,
            country.iso3 AS sent_currency
        FROM
            bank_and_beneficiary_info bank_and_ben
            JOIN countries country ON country.id = bank_and_ben.from_country_id
    ),
    get_received_currency_code AS (
        SELECT
            get_sent_curr.*,
            country.iso3 AS received_currency
        FROM
            get_sent_currency_code get_sent_curr
            JOIN countries country ON country.id = get_sent_curr.to_country_id
    )
SELECT
    rec.reference AS 'Transaction reference',
    rec.status AS 'Transaction status',
    rec.created_at AS 'Money sent date',
    rec.completed_at AS 'Money delivered date',
    rec.sent_currency AS 'Sent Currency code',
    rec.send_amount AS 'Sent amount',
    rec.account_name AS 'Sender Full Name',
    rec.othernames AS 'Sender Other names',
    rec.dob AS 'Sender DOB',
    rec.address_line_1 AS 'Sender Address',
    rec.suburb AS 'Sender Suburb',
    rec.state_name AS 'Sender State',
    rec.postcode AS 'Sender Postcode',
    rec.country_name AS 'Sender Country',
    rec.mobile_phone AS 'Sender Mobile number',
    rec.occupation AS 'Sender Occupation',
    rec.member_id AS 'Sender MemberID',
    rec.idtype_name AS 'Sender ID type',
    rec.idnumber AS 'Sender ID number',
    rec.issuer AS 'ID issuer',
    rec.ben_fullname AS 'Beneficiary Full name',
    rec.ben_address AS 'Address',
    rec.ben_phone AS 'Mobile phone number',
    rec.ben_country AS 'Country',
    rec.bank_name AS 'Bank name',
    rec.bank_location AS 'Bank Location',
    rec.account_number AS 'Account number',
    rec.received_amount AS 'Amount received',
    rec.sent_currency AS 'Currency code',
    rec.comment AS 'Reason',
    rec.payout_name AS 'Payout_gateway'
FROM
    get_received_currency_code rec;