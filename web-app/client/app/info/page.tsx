import { subtitle, title } from "@/components/primitives";

export default function InfoPage() {
  return (
    <>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <div className="inline-block max-w-lg text-center justify-center">
          <h2 className={subtitle({ class: "mt-4" })}>
            Welcome to the very early stages of Spotlight!. 
            
          </h2>
          <h2 className={subtitle({ class: "mt-4" })}>
            Spotlight aims to be a resource to journalists and researchers, and encourage civic engagement by making unslanted data easy to access, understand, and validate.
          </h2>
          <h2 className={subtitle({ class: "mt-4" })}>
            In alignment with Spotlight&apos;s spirit of transparency and open-data, it&apos;s an open-source project, and you can inspect and contribute to the code used to source the data it provides in its GitHub project, or make a contribution via pull request.
          </h2>
        </div>
      </ section>
    </>
  );
}
