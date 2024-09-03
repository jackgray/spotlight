'use client';

import React from "react";
import { Popover, PopoverTrigger, PopoverContent } from "@nextui-org/popover";
import { Button } from "@nextui-org/button";
import {Code} from "@nextui-org/code";


interface CodePopoverProps {
  popover_header: string,
  popover_text: string,
  button_text: string
}

const CodePopover: React.FC<CodePopoverProps> = ({ popover_header, popover_text, button_text }) => {
  return (
    <span>
      <Popover placement="bottom" showArrow={true}>
        <PopoverTrigger>
          <Button>{button_text}</Button>
        </PopoverTrigger>
        <PopoverContent>
          <div className="px-1 py-2">
            <div className="text-small font-bold">{popover_header}</div>
            <div className="text-tiny">{popover_text}</div>
            <Code size="sm">npm install @nextui-org/react</Code>
          </div>
        </PopoverContent>
      </Popover>
    </span>
  );
};

export default CodePopover;
