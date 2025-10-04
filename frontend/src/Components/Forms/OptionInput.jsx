import React from 'react';

export default function OptionInput({ value, onChange }) {
  return (
    <div>
      <input placeholder="옵션 입력" value={value} onChange={(e)=>onChange(e.target.value)} />
    </div>
  );
}