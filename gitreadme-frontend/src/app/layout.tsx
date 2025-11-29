import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "GitReadme - AI README Generator",
  description:
    "Turn your GitHub repositories into professional documentation using AI. Generate beautiful README.md files instantly using OpenAI.",
  keywords: [
    "README generator",
    "GitHub",
    "AI",
    "OpenAI",
    "documentation",
    "markdown",
    "repository",
  ],
  authors: [{ name: "GitReadme Team" }],
  creator: "GitReadme",
  publisher: "GitReadme",
  metadataBase: new URL("https://gitreadme.vercel.app"),

  openGraph: {
    title: "GitReadme - AI README Generator",
    description:
      "Generate clean and professional README.md files for any GitHub repository using AI.",
    url: "https://gitreadme.vercel.app",
    siteName: "GitReadme",
    type: "website",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "GitReadme - AI README Generator",
      },
    ],
  },

  twitter: {
    card: "summary_large_image",
    title: "GitReadme - AI README Generator",
    description:
      "Instantly create stunning README.md files with AI. Try GitReadme!",
    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
