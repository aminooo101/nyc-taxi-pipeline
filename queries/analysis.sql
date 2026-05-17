-- 1. Ingresos medios por hora del día
SELECT
  EXTRACT(HOUR FROM tpep_pickup_datetime) AS hora,
  ROUND(AVG(total_amount), 2) AS ingreso_medio,
  COUNT(*) AS num_viajes
FROM `midnight-495805.nyc_data.yellow_trips_final`
GROUP BY hora
ORDER BY hora;

-- 2. Top 10 distancias más frecuentes
SELECT
  ROUND(trip_distance, 0) AS distancia_millas,
  COUNT(*) AS viajes,
  ROUND(AVG(total_amount), 2) AS tarifa_media
FROM `midnight-495805.nyc_data.yellow_trips_final`
GROUP BY distancia_millas
ORDER BY viajes DESC
LIMIT 10;

-- 3. Comparativa método de pago
SELECT
  payment_type,
  COUNT(*) AS total_viajes,
  ROUND(AVG(tip_amount), 2) AS propina_media,
  ROUND(SUM(total_amount), 2) AS ingresos_totales
FROM `midnight-495805.nyc_data.yellow_trips_final`
GROUP BY payment_type
ORDER BY total_viajes DESC;
