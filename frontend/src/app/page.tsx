export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 text-center">
      <div className="max-w-2xl space-y-4">
        <div className="inline-block rounded-full bg-cyan-950/80 px-4 py-1 text-sm font-medium text-cyan-400 border border-cyan-800/50">
          FloodLens AI • Platform Foundation
        </div>
        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-slate-100">
          Explainable Urban Flood Susceptibility & Planning Decision-Support
        </h1>
        <p className="text-slate-400 text-base sm:text-lg">
          Frontend foundation initialized. Cesium 3D Globe and MapLibre geospatial visualization modules will be integrated during feature implementation.
        </p>
      </div>
    </main>
  );
}
