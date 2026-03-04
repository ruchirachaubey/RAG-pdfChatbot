"use client";

import { z } from "zod";
import UploadformInput from "./upload-form-input";
import { useUploadThing } from "@/utils/Uploadthing";
import { toast } from "sonner";
import { generatePdfSummary } from "@/actions/upload-actions";

const schema = z.object({
  file: z
    .instanceof(File, { message: "Invalid file" })
    .refine(
      (file) => file.size <= 20 * 1024 * 1024,
      "File size must be less than 20MB"
    )
    .refine(
      (file) => file.type === "application/pdf",
      "File must be a PDF"
    ),
});

export default function Uploadform() {
  const { startUpload } = useUploadThing("pdfUploader", {
    onClientUploadComplete: () => {
      console.log("Uploaded successfully!");
    },

    onUploadError: (err) => {
      console.error("Upload error:", err);

      toast.error("Upload failed", {
        description: err.message ?? "Something went wrong while uploading",
      });
    },

    onUploadBegin: ({ file }) => {
      console.log(`Uploading ${file}...`);
    },
  });

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const file = formData.get("file") as File;

    const validatedFields = schema.safeParse({ file });

    if (!validatedFields.success) {
      toast.error("Invalid file", {
        description:
          validatedFields.error.flatten().fieldErrors.file?.[0] ??
          "Please upload a valid PDF",
      });
      return;
    }

    toast.loading("Uploading PDF…");

    const resp = await startUpload([file]);

    if (!resp) {
      toast.error("Upload failed", {
        description: "Please try a different file",
      });
      return;
    }

    toast.success("Processing PDF", {
      description: "Hang tight! Our AI is reading your document 📄",
    });

    
    const summary = await generatePdfSummary(resp);
    console.log({ summary });
  };

  return (
    <div className="flex flex-col gap-8 w-full max-w-2xl mx-auto">
      <UploadformInput onSubmit={handleSubmit} />
    </div>
  );
}
