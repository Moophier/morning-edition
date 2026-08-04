"use client";

import { useEffect, useRef } from "react";

interface MapViewProps {
  coords: [number, number][];
  height?: number;
  waypointNames?: string[];
}

export default function MapView({ coords, height = 400, waypointNames }: MapViewProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<any>(null);

  useEffect(() => {
    import("leaflet").then(Lmod => {
      const L = Lmod.default;

      if (!mapRef.current || mapInstance.current) return;

      const map = L.map(mapRef.current, { zoomControl: false }).setView(coords[0] || [0, 0], 13);
      L.control.zoom({ position: "topleft" }).addTo(map);
      L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
        subdomains: "abcd", maxZoom: 19,
      }).addTo(map);

      L.polyline(coords, { color: "#5a9e7a", weight: 3, opacity: 0.7, dashArray: "8,6" }).addTo(map);

      coords.forEach((c, i) => {
        const color = i === 0 ? "#5a9e7a" : i === coords.length - 1 ? "#6888cc" : "#c9a24e";
        L.circleMarker(c, { radius: i === 0 || i === coords.length - 1 ? 8 : 6, fillColor: color, color, weight: 2, opacity: 0.8, fillOpacity: 0.6 })
          .addTo(map)
          .bindPopup(`<strong>${waypointNames?.[i] || `途经点 ${i + 1}`}</strong>`);
      });

      map.fitBounds(L.latLngBounds(coords).pad(0.15));
      mapInstance.current = map;
    });

    return () => {
      if (mapInstance.current) {
        mapInstance.current.remove();
        mapInstance.current = null;
      }
    };
  }, [coords, waypointNames]);

  return <div ref={mapRef} style={{ height, width: "100%", borderRadius: "8px" }} />;
}
