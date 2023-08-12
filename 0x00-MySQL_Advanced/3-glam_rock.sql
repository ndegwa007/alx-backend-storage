-- script list all bands with Glam rock style
SELECT band_name, 2022 - formed AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('glam rock', style)
ORDER BY lifespan DESC;
