export default function PolicalDonorsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <main className="container mx-auto max-w-full pt-2 px-2 flex-grow">
      {children}
    </main>
  );
}
