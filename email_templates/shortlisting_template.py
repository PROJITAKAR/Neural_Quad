
# This script generates an HTML email template for notifying students about their admission shortlist status.
def shortlisting_template(student_name: str) -> str:
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
                            <p>Congratulations! You have been <b>shortlisted</b> for admission at IEM.</p>
                            <p>Please find attached <b>Fee Structure</b> document for your reference.</p>
                            <p>Here are the next steps:</p>
                            <ul>
                                <li>Review the attached fee structure carefully.</li>
                                <li>Complete the required formalities by the given deadline.</li>
                                <li>Submit any pending documents, if applicable.</li>
                                <li>Reach out to admissions for further assistance.</li>
                            </ul>
                            <p>We look forward to welcoming you to IEM. For assistance, please email <b style="color: #007bff;">admissions@iemcollege.com</b>.</p>

                        </div>

                        <footer style="background-color: #ffffff; font-size: 14px; color: #666666; padding: 15px; text-align: center; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
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