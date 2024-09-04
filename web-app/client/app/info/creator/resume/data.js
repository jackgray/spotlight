
export const CVData = {
    personalData: {
      name: 'Jack Gray',
      title: 'Full Stack Data Platform Engineer',
      // image: '',
      contacts: [
        { type: 'email', value: 'contact@jackgray.nyc' },
        { type: 'phone', value: '929-409-5452' },
        { type: 'location', value: 'Brooklyn, New York' },
        { type: 'website', value: 'beta.spotlight-us.com' },
        { type: 'linkedin', value: 'linkedin.com/in/johnhgrayiii' },
        // { type: 'twitter', value: 'twitter.com/sbayd' },
        { type: 'github', value: 'github.com/jackgray' }
      ]
    },
    sections: [
      {
        type: 'text',
        title: 'Career Profile',
        content: `
While my formal degrees are in computers and electrical hardware, I have always maintained web development and data automation as a hobby. In 2016 that received a boost, as I sought expressive outlets I could use to confront the issues that impassion me. 
For 4 years, I religiously focused on full-stack React development and graph based relational models. 
During this time, I was able to apply previous analytical skills in Python and Linux along with some I was acquiring such as containerization, cloud technologies, distributed system designs, and network security to develop tools and optimize data pipelines for researchers. 
To gain more ownership and responsibility, I undertook the task of managing technical operations for a brain research lab at Mount Sinai, where my appreciation for the ability of data to shape policy, medical advancements and culture proliferated.
Recently, my passions have expanded towards financial market transparency, and I have leveraged my abilities in data extraction, infrastructure design, and application development to build a bespoke platform to collect and distribute regulatory and other oversight-focused datasets.
Between my personal and professional projects, out of necessity, my experience spans the full spectrum of container-based data infrastructure and application design, allowing me to tackle a diverse array of challenges. 
I thrive in environments where understanding the inter-play of disparate component in complex systems is essential and a creative and philosophical approach to designing solutions and solving problems are more important than speed of implementation. 
        `,
        icon: 'usertie'
      },
      {
        type: 'common-list',
        title: 'Education',
        icon: 'graduation',
        items: [
          {
            title: 'Electrical Engineering, B.Eng (Minor in Neuroscience)',
            authority: 'Auburn University',
            authorityWebSite: 'https://eng.auburn.edu/ece/#gsc.tab=0',
            rightSide: '2009 - 2014'
          },
          {
            title: 'Meta Data Engineer Professional Certificate',
            authority: 'Meta',
            authorityWebSite: 'https://www.linkedin.com/in/johnhgrayiii'
          },
          {
            title: 'IBM Professional Software Developer Professional Certificate',
            authority: 'IBM',
            authorityWebSite: 'https://www.linkedin.com/in/johnhgrayiii',
            rightSide: 'test'
          }
        ]
      },
      {
        type: 'experiences-list',
        title: 'Experiences',
        description: 'Optional',
        icon: 'archive',
        items: [
          {
            title: 'Head of Data & Engineering',
            company: 'Brain Research Center @ Mount Sinai',
            description: `
- Oversee all data and related technology for 6 active clinical trials and more than 10 prior studies, including compute infrastructure, database modeling/management, ETL/ELT pipelines, and web service development and hosting
-  Wrangled > 50TB debt of unstructured text, audio, and neuro-imaging data 
-  Designed  bare metal/cloud hybrid computing cluster and IaC node provisioning using Terraform, Make, Bash, & systemd templates for RHEL CoreOS to produce faster/lighter K8 alternative with low attack surface 
-  Built on-prem tiered distributed object data lake supporting git remotes, container registry, web app storage, databases, large files, ElasticSearch indices, and ETL staging, modernizing data infrastructure while maintaining HIPAA compliance,  high security standards, and scalability 
-  Build batch processing DAG data pipelines in SQL, Bash, and Python, and manage distributed scheduling platform (Kestra) 
-  Configure and manage ElasticSearch to load logs, system metrics, and unstructured documents into free-text searchable indices 
-  Automate fMRI processing and time-series alignment of longitudinal data 
-  Model clinical assessment data for relational and graph dbs 
-  Develop and maintain multi-tenant virtual workspace solution offering scalable and portable computing environments with RBAC data access and pre-configured analysis software 
-  Develop and host full stack JavaScript  web applications, enabling daily remote data collection from subject mobile devices, increasing data resolution 
-  Create visual dashboards of data and system metrics in Kibana and Apache Superset
            `,
            companyWebSite: 'https://icahn.mssm.edu/research/narc',
            companyMeta: '',
            datesBetween: '2022 - Present',
            descriptionTags: ['DB/Large file hosting', 'ETL/ELT', 'Service hosting/security', 'Data alignment', 'Grant writing']
          },
          {
            title: 'Data Engineer',
            company: 'Columbia Psychiatry / New York State Psychiatric Institute',
            description: 'Developed tools to quality-check, transform, and load data between research MRI console and analysis cluster. Built automation pipelines to pre-process neuro-imaging data.',
            companyWebSite: 'http://nyspi.org',
            companyMeta: 'MRI Brain Imaging Center',
            datesBetween: '2021 - 2022'
          },
          {
            title: 'Research Engineer',
            company: 'Columbia Psychiatry / New York State Psychiatric Institute',
            description: 'I was warming up.',
            companyWebSite: 'http://someexamplecompany.com',
            companyMeta: 'MRI Brain Imaging Center',
            datesBetween: '2016 - 2021'
          }
        ]
      },
      {
        type: 'projects-list',
        title: 'Projects',
        description: 'Some projects I mostly use as a learning canvas, but I hope will someday become into useful tools.',
        icon: 'tasks',
        groups: [
          {
            items: [
              { title: 'Spotlight', projectUrl: 'beta.spotlight-us.com', description: 'Data aggregation platform geared towards regulatory oversight and transparency' },
              { title: 'Vapetaper', projectUrl: 'github.com/jackgray/vapetaper', description: 'Easily track usage of substances like vapes without manual logging' },
              { title: 'Voxemo', projectUrl: 'github.com/jackgray/voxemo', description: 'Convert emotional sentiment across mediums. Turn a audio-diary recording into a song or picture, stream a soundtrack reflecting things passively detected in your environment.' }
            ]
          }
        ]
      },
      {
        type: 'common-list',
        title: 'Publications',
        description: '',
        icon: 'comments',
        items: [
          {
            title: 'Something',
            authority: 'Nature Neuroscience',
            authorityWebSite: 'https://www.linkedin.com/in/johnhgrayiii'
          },
          {
            title: 'Another',
            authority: 'JAMA Psychiatry',
            authorityWebSite: 'https://www.linkedin.com/in/johnhgrayiii',
            rightSide: '2024'
          }
        ]
      },
      {
        type: 'tag-list',
        title: 'Skills Proficiency',
        icon: 'rocket',
        items: ['Python', 'Linux/Bash', 'ETL/ELT', 'Docker', 'Terraform', 'Apache Superset', 'Airflow', 'S3', 'Clickhouse', 'Data lakehouse design', 'React', 'Javascript', 'Next.js', 'GraphQL', 'SQL']
      },
      {
        type: 'tag-list',
        title: 'Hobbies & Interests',
        icon: 'cubes',
        items: ['Music', 'Home Lab/Home Automation', 'Cycling/Skating', 'Animal Rescue', 'Financial Market Transparency', 'Mental Health Research/Tech', 'Tennis/Volleyball']
      }
    ]
  }