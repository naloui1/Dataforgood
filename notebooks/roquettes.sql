WITH data_union AS (
    SELECT 
        "libelle_geographique" AS "Nom commune principale",
        CAST("code_insee" AS INTEGER) AS "Code Insee commune",
        "Région",
        "Département",
        CAST("Code Postal" AS INTEGER) AS "Code Postal",
        "Type équipement ou lieu" AS "Type",
        "Nom" AS "Nom d'evenement",
        "Latitude",
        "Longitude",
        "Nombre_ecrans",
        "Nombre_fauteuils_de_cinema",
        "Nombre_de_salles_de_theatre"
    FROM basilics_data bd
    UNION
    SELECT
        "Commune principale de déroulement" AS "Nom commune principale",
        CAST("Code Insee commune" AS INTEGER) AS "Code Insee commune",
        "Région principale de déroulement" AS "Région",
        "Département principal de déroulement" AS "Département",
        CAST("Code postal (de la commune principale de déroulement)" AS INTEGER) AS "Code Postal",
        "Discipline dominante" AS "Type",
        "Nom du festival",
        SUBSTR("Géocodage xy", 1, INSTR("Géocodage xy", ',') - 1) AS Latitude,
        SUBSTR("Géocodage xy", INSTR("Géocodage xy", ',') + 1) AS Longitude,
        CAST('' as INT) as "Nombre_ecrans",
        CAST('' as INT) as "Nombre_fauteuils_de_cinema",
        CAST('' as INT) as "Nombre_de_salles_de_theatre"
    FROM festivals_data fd
)
SELECT DISTINCT 
    dt."Nom commune principale" ,
    dt."Code Insee commune",
    dt."Région",
    dt."Département",
    dt."Code Postal",
    vd.latitude as "commune_latitude",
    vd.longitude as "commune_longtitude",
    dt."Type",
    dt."Nom d'evenement",
    dt."Latitude" as "etb_latitude",
    dt."Longitude" as "etb_longtitude",
    pd.PTOT,
    CASE 
        WHEN EXISTS (SELECT 1 FROM villes_data vd WHERE vd.insee_com = dt."Code Insee commune") 
        THEN 'oui' 
        ELSE 'non' 
    END AS "Petite commune",
    cat.Category,
    CASE 
        WHEN dt."Type" = 'Cinéma' THEN dt."Nombre_ecrans"
        ELSE NULL 
    END AS n_ecrans_cinema,
    CASE 
        WHEN dt."Type" = 'Cinéma' THEN dt."Nombre_fauteuils_de_cinema"
        ELSE NULL 
    END AS n_fauteuils_cinema ,
    CASE 
        WHEN dt."Type" = 'Théâtre' THEN dt."Nombre_de_salles_de_theatre"
        ELSE NULL 
    END AS n_salles_theatre   
FROM data_union dt
LEFT JOIN population_data pd
    ON pd.COM = dt."Code Insee commune"
LEFT JOIN categories_evenements_data cat
    ON dt.Type = cat."Nom events"
LEFT JOIN centre_villes_data vd
	ON vd."code_commune_INSEE" = dt."Code Insee commune"
    