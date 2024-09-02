import React from 'react';

import ReactCV from 'react-cv';
import { CVData } from './data';



const ResumePage = () => {
    return (
        <div>
           <ReactCV {...CVData} />
        </div>
    );
};

export default ResumePage;
