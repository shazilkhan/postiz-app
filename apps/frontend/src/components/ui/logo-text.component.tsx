import React from 'react';

export const LogoTextComponent = () => {
  return (
    <div className="flex items-center gap-[6px]">
      <svg
        width="44"
        height="44"
        viewBox="0 0 96 96"
        fill="none"
        stroke="#D00314"
        strokeWidth="7.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path d="M56 28V42A9.35 9.35 0 0 0 74.7 42A27 27 0 1 0 25.09 52.29L48 89L60.83 68.44" />
        <circle cx="46.5" cy="38" r="9.5" />
      </svg>
      <div className="flex gap-[6px] text-[24px] leading-none tracking-[-0.035em]">
        <span className="font-[700]">GeoScribe</span>
        <span className="font-[500] text-[#FF7065]">Social</span>
      </div>
    </div>
  );
};
