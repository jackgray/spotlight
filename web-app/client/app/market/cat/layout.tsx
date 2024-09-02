export default function MarketCatDataLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <main className="container mx-auto max-w-full pt-6 px-2 flex-grow">
      {children}
    </main>
  );
}
