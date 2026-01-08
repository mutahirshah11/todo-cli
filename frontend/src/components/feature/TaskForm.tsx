import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { taskSchema, TaskFormValues } from '@/lib/schemas';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface TaskFormProps {
  onSubmit: (data: TaskFormValues) => void;
  defaultValues?: Partial<TaskFormValues>;
  submitButtonText?: string;
}

export const TaskForm: React.FC<TaskFormProps> = ({
  onSubmit,
  defaultValues = {},
  submitButtonText = 'Submit'
}) => {
  const form = useForm<TaskFormValues>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: defaultValues.title || '',
      description: defaultValues.description || '',
      is_completed: defaultValues.is_completed || false,
    }
  });

  const handleSubmit = (data: TaskFormValues) => {
    onSubmit(data);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{defaultValues.title ? 'Edit Task' : 'Create New Task'}</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Title *</FormLabel>
                  <FormControl>
                    <Input placeholder="Task title" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Task description (optional)"
                      {...field}
                      value={field.value || ''}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button type="submit" disabled={form.formState.isSubmitting}>
              {form.formState.isSubmitting ? 'Submitting...' : submitButtonText}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};