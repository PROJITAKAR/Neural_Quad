
# This code defines a function that generates an HTML email template for notifying students who have not been shortlisted for admission.
def Not_Shortlisted_template(student_name: str) -> str:
    return f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Admission Shortlist Notification</title>
                </head>

                <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4;">
                    <div style="max-width: 600px; background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin: auto;">
                        <header style="background-color: #007bff; color: #ffffff; text-align: center; padding: 15px; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                            <h1 style="font-size: 22px; margin: 0;"><b>Institute of Engineering & Management (IEM)</b></h1>
                            <p style="font-size: 14px; margin: 5px 0 0;">Admission Shortlist Notification</p>
                        </header>

                        <div style="padding: 20px; font-size: 16px; color: #333333; line-height: 1.5;">
                        
                            <h2>Dear {student_name},</h2>
                            <p>Thank you for applying to IEM. After careful review, we regret to inform you that you have <b>not been shortlisted</b> for admission.</p>
            
                            <p>We encourage you to:</p>
                            <ul style="padding-left: 18px;">
                                <li>Apply in the next admission cycle.</li>
                                <li>Contact admissions for guidance.</li>
                            </ul>
                            
                            <p>We appreciate your interest and wish you success in your academic journey. For queries, contact <b style="color: #007bff;">admissions@iemcollege.com</b>.</p>

                        </div>

                        <footer style="background-color: #f1f1f1; font-size: 14px; color: #666666; padding: 15px; text-align: center; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                            <p>This is a <b>no-reply email</b>. If you have any queries, please reach out to:</p>
                            <p><b>Email:</b> <a href="mailto:admissions@iem.edu.in" style="color: #007bff; text-decoration: none;">admissions@iem.edu.in</a></p>
                            <p><b>Phone:</b> +91-XXXXXXXXXX</p>
                            <p>Visit our website: <a href="https://www.iem.edu.in" style="color: #007bff; text-decoration: none;">www.iem.edu.in</a></p>
                            <p>We look forward to having you with us!</p>
                        </footer>
                    </div>
                </body>
                </html>
                """
