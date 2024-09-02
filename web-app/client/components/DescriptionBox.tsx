'use client'

import React from "react";
import {Textarea} from "@nextui-org/input";

interface DescriptionBoxProps {
    label: string,
    text: string
  }

const DescriptionBox: React.FC<DescriptionBoxProps> = ({ label, text }) => {
  return (
    <Textarea
      isDisabled
      label={label}
      labelPlacement="outside"
      placeholder="Enter your description"
      defaultValue={text}
      className="max-w-xs"
    />
  );
}

 export default DescriptionBox;