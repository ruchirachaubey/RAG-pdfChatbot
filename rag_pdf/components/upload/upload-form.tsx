"use client";

import { useState } from "react";
import UploadformInput from "./upload-form-input";
import { z } from "zod";
import { useUploadThing } from "@/utils/Uploadthing";
import { toast } from "sonner";
import { generatePdfSummary } from "@/actions/upload-actions";


const schema = z.object({
  file: z
    .instanceof(File, { message: "Invalid file" })
    .refine((file) => file.size <= 20 * 1024 * 1024, "File size must be less than 20MB")
    .refine((file) => file.type === "application/pdf", "File must be a PDF"),
});

export default function Uploadform() {

  const { startUpload } = useUploadThing("pdfUploader", {
    onClientUploadComplete: () => {
      toast.success("Uploaded successfully!");
    },

    onUploadError: (err) => {
      toast.error(err.message);
    },

    onUploadBegin: ({ fileName }) => {
      toast.loading(`Uploading ${fileName}...`);
    },
  });

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const file = formData.get("file") as File;

    const validatedFields = schema.safeParse({ file });

    if (!validatedFields.success) {
      toast.error(
        validatedFields.error.flatten().fieldErrors.file?.[0] ??
          "Invalid file"
      );
      return;
    }

    const resp = await startUpload([file]);

    if (!resp) {
      toast.error("Please use a different file");
      return;
    }

    toast.success("Processing PDF. Please wait!");
  

  const summary = await generatePdfSummary(resp);

};

  return (
    <div className="flex flex-col gap-8 w-full max-w-2xl mx-auto">
      <UploadformInput onSubmit={handleSubmit} />
    </div>
  );
}
