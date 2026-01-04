import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Panaceya - Democratizing Surgical Excellence',
  description: 'Experience the future of surgical training with AI-powered coaching, realistic physics simulation, and gamified learning.',
  keywords: 'surgical training, AI coaching, medical education, virtual surgery, SOFA simulation',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
