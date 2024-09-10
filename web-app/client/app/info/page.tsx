import { subtitle, title } from "@/components/primitives";

export default function InfoPage() {
  return (
    <>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <div className="inline-block max-w-lg text-center justify-center">
          <h2 className={subtitle({ class: "mt-4" })}>
            Welcome to the very early stages of Spotlight! The most dangerous people to society are . They commit crimes and abuse power in broad daylight healthcare access and legislation to global economy. 
            
          </h2>
          <h2 className={subtitle({ class: "mt-4" })}>
            Spotlight aims to be a resource to journalists and researchers, and encourage civic engagement by making unslanted data easy to access, understand, and validate.
          </h2>
          <h2 className={subtitle({ class: "mt-4" })}>
            Dealings which are supposed to represent the interest of the people, or risk economic health and result in taxpayer bail-outs should not be made in the shadows. This project attempts to point a spotlight on those dealings which are meant to be for the betterment of society, but are often instead at its expense.
          </h2>
          <h2 className={subtitle({ class: "mt-4" })}>
            In alignment with Spotlight&apos;s spirit of transparency and open-data, it&apos;s an open-source project, and you can inspect and contribute to the code used to source the data it provides in its GitHub project. Contact me at contact@jackgray.nyc if you want to know what I need help with the most, or simply make a pull request on the GitHub project.
          </h2>
        </div>
      </ section>
    </>
  );
}
