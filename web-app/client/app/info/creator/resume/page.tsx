import {FC} from 'react';
import ReactCV from 'react-cv';
import { CVData } from './data';


const ResumePage: FC = () => {
    return (
        <div>
           <ReactCV {...CVData} />
        </div>
    );
};

export default ResumePage;
