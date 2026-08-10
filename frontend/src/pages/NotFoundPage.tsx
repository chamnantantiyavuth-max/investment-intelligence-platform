import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"

export default function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center">
      <h1 className="text-6xl font-bold text-muted-foreground/30">404</h1>
      <h2 className="mt-4 text-lg font-semibold">Page not found</h2>
      <p className="mt-2 text-sm text-muted-foreground">
        The page you're looking for doesn't exist.
      </p>
      <Button className="mt-6" render={<Link to="/" />}>
        Back to Dashboard
      </Button>
    </div>
  )
}
