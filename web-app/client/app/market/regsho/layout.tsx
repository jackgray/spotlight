export default function MarketRegShoDataLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <main className="container mx-auto max-w-7xl pt-6 px-2 flex-grow">
      {children}
    </main>
  );
}
