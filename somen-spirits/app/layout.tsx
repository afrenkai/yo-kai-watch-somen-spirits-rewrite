import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Yo-kai Watch Somen Spirits",
  description: "Yo-kai Watch fan game",
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
