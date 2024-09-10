
export const CVData = {
    personalData: {
      name: 'Jack Gray',
      title: 'Full Stack / Data Platform Engineer',
      contacts: [
        { type: 'email', value: 'contact@jackgray.nyc' },
        { type: 'phone', value: '929-409-5452' },
        { type: 'location', value: 'Brooklyn, New York' },
        { type: 'website', value: 'beta.spotlight-us.com' },
        { type: 'linkedin', value: 'linkedin.com/in/johnhgrayiii' },
        { type: 'github', value: 'github.com/jackgray' }
      ]
    },
    sections: [
      {
        type: 'text',
        title: 'Bio',
        content: `
I use technology as an expressive device to confront the issues that I care about. It allows me to convert my negative energy from society's ailments into constructive learning experiences and hopes of making meaningful contributions to whatever cause I'm focusing on.
My experience spans a wide range of container-based data infrastructure and application designs, enabling me to address diverse challenges, and bridge the gap between academic research science and modern data strategies and platform designs in a clinical research context. 

I thrive in environments where understanding the interplay of complex systems is crucial, and a creative and thoughtful approach to solution design is valued over rapid implementation.
While my professional focus for nearly a decade has been based in clinical psych research, I've maintained a growing personal interest in policy and financial markets, the mechanisms that drive them, and the extent to which they are shaped or manipulated by personal interests and abuse of power. 
This was the essence behind my motivation to become proficient in web app design--to be able to single handedly actualize the solutions I imagined for the world's problems. 
Data drives policy and culture. And technology affects how people interact with it and each other. My mission is to leverage as many of my assets as possible to create tools that could affect the change I wish to see.
The culmination of much of my studies in data engineering, infrastructure, and React development from the past 8 years is presented in my project, <a href=github.com/jackgray/spotlight'>Spotlight</a>, 
a bespoke platform for aggregating and distributing regulatory and oversight-focused datasets, encompassing of architectural designs, infrastructure code, and hardware to host client applications, big data, and processing pipelines in a distributed, scalable, and highly available environment.
        `,
        icon: ' usertie'
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
            companyMeta: 'Neuropsychoimaging of Addiction and Related Conditions (NARC)',
            datesBetween: '2022 - Present',
            descriptionTags: ['DB/Large file hosting', 'ETL/ELT', 'Service hosting/security', 'Data alignment', 'Grant writing']
          },
          {
            title: 'Data Engineer & MRI Technical Specialist',
            company: 'Columbia Psychiatry / New York State Psychiatric Institute',
            description: 'Developed tools to quality-check, transform, and load data between research MRI console and analysis cluster. Built automation pipelines to pre-process neuro-imaging data.',
            companyWebSite: 'http://nyspi.org',
            companyMeta: 'MRI Brain Imaging Center',
            datesBetween: '2021 - 2022'
          },
          {
            title: 'Research Imaging Engineer',
            company: 'Columbia Psychiatry / New York State Psychiatric Institute',
            description: 'Worked alongside clinical researchers and engineers to maintain and improve technical components and processes of the MRI research center, ranging from data transformations, MRI hardware and software, physiologic recording methods, and patient interaction.',
            companyWebSite: 'http://someexamplecompany.com',
            companyMeta: 'MRI Brain Imaging Center',
            datesBetween: '2016 - 2021'
          }
        ]
      },
      {
        type: 'projects-list',
        title: 'Projects',
        description: 'I mostly use my projects as a learning canvas, but hope one or two will someday become into useful tools.',
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
            title: 'Recovery of anterior prefrontal cortex inhibitory control after 15 weeks of inpatient treatment in heroin use disorder',
            authority: 'Nature Mental Health',
            authorityWebSite: 'https://www.nature.com/articles/s44220-024-00230-4'
          },
          {
            title: 'Neuromelanin-sensitive MRI as a noninvasive proxy measure of dopamine function in the human brain',
            authority: 'PNAS - Proceedings of the National Academy of Sciences',
            authorityWebSite: 'https://www.pnas.org/doi/full/10.1073/pnas.1807983116',
            rightSide: '*Unaccredited contributor'
          },
          {
            title: 'Breakdown and optical emission characteristics of point-to-point electrodes subject to pulsed 20kHz applied field in sub-atmospheric pressure N2-He gas mixtures',
            authority: 'IEEE',
            authorityWebSite: 'https://ieeexplore.ieee.org/document/7287307/',
          },
          {
            title: '20 kHz unipolar pulsed field surface flashover characteristics of polymer nanocomposites in subatmospheric pressure helium',
            authority: 'IEEE',
            authorityWebSite: 'https://ieeexplore.ieee.org/document/7287308',
            rightSide: '*Unaccredited contributor'
          },
        ]
      },
      {
        type: 'tag-list',
        title: 'Skills Proficiency',
        icon: 'rocket',
        items: ['Python','SQL', 'OLAP/OLTP', 'Linux/Bash', 'ETL/ELT', 'Docker', 'AWS', 'Azure', 'Terraform', 'Clickhouse', 'Apache Superset', 'Kafka',  'DAG Scheduling', 'Elastic Stack', 'S3', 'Clickhouse', 'Distributed System Design', 'React', 'Javascript', 'Next.js', 'GraphQL', 'REST', 'Experimental Design', 'Neuroanalysis', 'fMRIPrep', 'DICOM/nifti formats', 'BIDS', 'ePrime/jsPsych']
      },
      {
        type: 'tag-list',
        title: 'Hobbies & Interests',
        icon: 'cubes',
        items: ['Web3', 'Music', 'Home Lab/Home Automation', 'Animal Rescue', 'Financial Market Transparency', 'Mental Health Research/Tech']
      }
    ]
  }